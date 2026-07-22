"""
Feature Engineering Agent.
Coordinates environmental observations aggregation and triggers tabular feature vectors calculation.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from backend.app.agents.base import BaseAgent
from backend.app.types import AgentResult, ProviderResult
from backend.app.core.config import settings
from backend.app.core.mongodb import get_collection
from backend.app.constants import Collections

# Import pipeline and database services
from backend.app.services.feature_pipeline import FeaturePipeline
from backend.app.services.feature_store_service import FeatureStoreService
from backend.app.utils.distance import haversine_distance

logger = logging.getLogger("aqintel.agents.featureengineering")

class FeatureEngineeringAgent(BaseAgent):
    """
    Coordinates feature extraction. Bypasses ML weight assumptions and delegates
    DB commits to FeatureStoreService.
    """

    def __init__(self) -> None:
        super().__init__(name="FeatureEngineeringAgent")
        self.store_service = FeatureStoreService()

    async def execute(self, *args, **kwargs) -> AgentResult:
        """
        Runs the feature engineering run.
        Accepts:
          - target_time: datetime (defaults to current utcnow)
          - station_id: Optional[str] (limits run to specific station, else runs all in city)
          - latitude: Optional[float] (for real-time coordinates)
          - longitude: Optional[float] (for real-time coordinates)
        """
        target_time = kwargs.get("target_time", datetime.utcnow())
        station_id_limit = kwargs.get("station_id")
        lat = kwargs.get("latitude")
        lon = kwargs.get("longitude")
        is_city_query = kwargs.get("is_city_query", False)
        
        self.logger.info(f"FeatureEngineeringAgent: executing for target_time={target_time}")
        
        try:
            if lat is not None and lon is not None:
                lat = float(lat)
                lon = float(lon)
                self.logger.info(f"FeatureEngineeringAgent: Dynamic execution path for coordinates ({lat}, {lon}), city_query={is_city_query}")
                
                # 1 & 2. Get optimal observation and execution plan via Data Availability Engine
                from backend.app.services.data_availability import DataAvailabilityEngine
                da_engine = DataAvailabilityEngine()
                
                obs_obj, plan = await da_engine.get_best_observation(lat, lon, is_city_query=is_city_query)
                aq_metrics = obs_obj.model_dump()
                # Ensure the legacy keys exist for downstream compatibility
                aq_metrics["aqi"] = obs_obj.final_aqi
                aq_metrics["source"] = obs_obj.provider
                for k, v in obs_obj.pollutants.model_dump().items():
                    if v is not None:
                        aq_metrics[k] = v

                    
                # 3. Fetch Weather dynamically using Adapter
                from backend.app.providers.weather import WeatherProvider
                wp = WeatherProvider()
                weather_metrics = {}
                if plan.weather_provider == "OpenWeather":
                    res = await wp.fetch(lat, lon, settings.OPENWEATHER_API_KEY)
                    if wp.validate(res):
                        normalized = wp.normalize(res)
                        weather_metrics = normalized.records[0]["metrics"] if normalized.records else {}
                        
                if not weather_metrics:
                    logger.warning(
                        f"FeatureEngineeringAgent: OpenWeather unavailable for ({lat}, {lon}). "
                        f"Using hardcoded weather defaults — temperature=25, humidity=50, wind=2 m/s."
                    )
                    weather_metrics = {
                        "temperature": 25.0,
                        "humidity": 50.0,
                        "wind_speed": 2.0,
                        "wind_direction": 90.0,
                        "precipitation": 0.0,
                        "pressure": 1013.0
                    }
                    
                # 4. GIS Metrics — OSMnx not available in real-time path; using estimation defaults
                logger.warning(
                    f"FeatureEngineeringAgent: GIS metrics hardcoded for ({lat}, {lon}). "
                    f"No live OSMnx fetch performed. Values: road_density=0.5 (urban estimate), "
                    f"industrial_distance=2000m (urban estimate), green_cover=0.2."
                )
                gis_metrics = {
                    "road_density": 0.5,
                    "industrial_distance": 2000.0,
                    "green_cover": 0.2,
                    "landuse": "residential",
                    "water_body_distance": 1000.0,
                    "nearest_highway": "Primary"
                }

                # 5. Active Fire Metrics — NASA FIRMS not queried; assuming no active fire
                logger.warning(
                    f"FeatureEngineeringAgent: Fire metrics hardcoded for ({lat}, {lon}). "
                    f"No NASA FIRMS API call performed. Assuming no active fire in vicinity."
                )
                fire_metrics = {
                    "fire_count": 0,
                    "nearest_fire_distance": 10000.0,
                    "nearest_fire_bearing": 0.0,
                    "average_frp": 0.0,
                    "maximum_frp": 0.0
                }

                # 6. Activity Metrics — No live traffic API; using urban average estimates
                logger.warning(
                    f"FeatureEngineeringAgent: Activity metrics hardcoded for ({lat}, {lon}). "
                    f"No live traffic API queried. Using urban average estimates."
                )
                activity_metrics = {
                    "traffic_density_score": 0.5,
                    "heavy_vehicle_score": 0.3,
                    "construction_score": 0.2,
                    "road_congestion_score": 0.4
                }
                
                # 7. Lag & History calculation
                hist_pm25 = []
                hist_aqi = []
                prev_aqi_1h = None
                if plan.has_history:
                    hist_pm25, hist_aqi, prev_aqi_1h = await self._fetch_history(
                        aq_metrics.get("station_id", "station"),
                        target_time
                    )
                    
                # 8. Build dynamic feature vector
                feature_vector = FeaturePipeline.process(
                    timestamp=target_time,
                    latitude=lat,
                    longitude=lon,
                    station_id=aq_metrics.get("station_id", "station"),
                    weather_metrics=weather_metrics,
                    gis_metrics=gis_metrics,
                    fire_metrics=fire_metrics,
                    current_aq=aq_metrics,
                    activity_metrics=activity_metrics,
                    historical_pm25=hist_pm25,
                    historical_aqi=hist_aqi,
                    prev_aqi_1h=prev_aqi_1h,
                    station_distance=aq_metrics.get("station_distance", 0.0),
                    source_record_ids=[]
                )
                
                return AgentResult(
                    agent_name=self.name,
                    success=True,
                    data={
                        "feature_vector": feature_vector,
                        "execution_plan": plan.model_dump(),
                        "observation": obs_obj.model_dump()
                    }
                )

            # --- DB batch path (original) ---
            # 1. Fetch CAAQMS records in the target timeframe (+/- 15 minutes freshness)

            # CAAQMS is the primary trigger. Feature vectors are aligned to CAAQMS readings.
            col = get_collection(Collections.NORMALIZED_ENVIRONMENT)
            if col is None:
                raise RuntimeError("Database collection handle is not connected.")

            query_filter = {
                "provider": "caaqms",
                "timestamp": {
                    "$gte": target_time - timedelta(minutes=15),
                    "$lte": target_time + timedelta(minutes=15)
                }
            }
            if station_id_limit:
                query_filter["metadata.station_id"] = station_id_limit

            cursor = col.find(query_filter)
            caaqms_records = await cursor.to_list(length=100)

            if not caaqms_records:
                msg = f"No primary CAAQMS records found within freshness limits (+/- 15m) of {target_time}."
                self.logger.warning(msg)
                return AgentResult(
                    agent_name=self.name,
                    success=True,
                    data={"message": msg, "processed_count": 0}
                )

            processed_count = 0
            feature_docs = []

            for caaqms_rec in caaqms_records:
                station_id = caaqms_rec.get("metadata", {}).get("station_id")
                rec_timestamp = caaqms_rec.get("timestamp")
                loc = caaqms_rec.get("location", {})
                lat = loc.get("latitude")
                lon = loc.get("longitude")

                if not lat or not lon:
                    self.logger.warning(f"Skipping record with missing location coordinates: {caaqms_rec}")
                    continue

                # 2. Query other provider metrics respecting freshness thresholds
                # - Weather (30 min freshness)
                weather_rec = await self._get_freshest_record("weather", rec_timestamp, 30)
                
                # - Fire (60 min freshness)
                fire_rec = await self._get_freshest_record("fire", rec_timestamp, 60)
                
                # - GIS (24h freshness = 1440 mins)
                gis_rec = await self._get_freshest_record("osm", rec_timestamp, 1440)
                
                # - Activity / simulated mobility indices (15m freshness)
                activity_rec = await self._get_freshest_record("activity", rec_timestamp, 15)

                # Expose metrics structures
                weather_metrics = weather_rec.get("metrics", {}) if weather_rec else {}
                gis_metrics = gis_rec.get("metrics", {}) if gis_rec else {}
                fire_metrics = fire_rec.get("metrics", {}) if fire_rec else {}
                current_aq = caaqms_rec.get("metrics", {})
                activity_metrics = activity_rec.get("metrics", {}) if activity_rec else {}

                # 3. Query historical CAAQMS readings for rolling indices (over past 24 hours)
                hist_pm25, hist_aqi, prev_aqi_1h = await self._fetch_history(station_id, rec_timestamp)

                # 4. Sensor Fusion: Calculate distance to station
                # Since we are processing at a station, distance is 0.0.
                station_distance = 0.0

                # 5. Extract lineage ids
                source_record_ids = [
                    str(caaqms_rec["_id"])
                ]
                if weather_rec:
                    source_record_ids.append(str(weather_rec["_id"]))
                if fire_rec:
                    source_record_ids.append(str(fire_rec["_id"]))
                if gis_rec:
                    source_record_ids.append(str(gis_rec["_id"]))
                if activity_rec:
                    source_record_ids.append(str(activity_rec["_id"]))

                # 6. Execute calculation pipeline
                feature_vector = FeaturePipeline.process(
                    timestamp=rec_timestamp,
                    latitude=lat,
                    longitude=lon,
                    station_id=station_id,
                    weather_metrics=weather_metrics,
                    gis_metrics=gis_metrics,
                    fire_metrics=fire_metrics,
                    current_aq=current_aq,
                    activity_metrics=activity_metrics,
                    historical_pm25=hist_pm25,
                    historical_aqi=hist_aqi,
                    prev_aqi_1h=prev_aqi_1h,
                    station_distance=station_distance,
                    source_record_ids=source_record_ids
                )

                # 7. Write via Store Service
                await self.store_service.save_feature_vector(feature_vector)
                
                feature_docs.append(feature_vector.model_dump(mode="json"))
                processed_count += 1

            return AgentResult(
                agent_name=self.name,
                success=True,
                data={
                    "processed_count": processed_count,
                    "processed_stations": [f.get("station_id") for f in feature_docs]
                }
            )

        except Exception as e:
            err_msg = f"FeatureEngineeringAgent execution failed: {e}"
            self.logger.error(err_msg, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                success=False,
                error_message=err_msg
            )

    async def _get_freshest_record(self, provider: str, target_time: datetime, max_delta_minutes: int) -> Optional[dict]:
        """
        Retrieves the temporally closest record for the provider within the freshness limits.
        """
        col = get_collection(Collections.NORMALIZED_ENVIRONMENT)
        if col is None:
            return None
            
        start_time = target_time - timedelta(minutes=max_delta_minutes)
        end_time = target_time + timedelta(minutes=max_delta_minutes)

        try:
            cursor = col.find({
                "provider": provider,
                "timestamp": {"$gte": start_time, "$lte": end_time}
            })
            records = await cursor.to_list(length=50)
            if not records:
                return None
            # Return record with the minimum temporal delta
            return min(records, key=lambda r: abs((r["timestamp"] - target_time).total_seconds()))
        except Exception as e:
            self.logger.warning(f"Error querying freshest record for provider '{provider}': {e}")
            return None

    async def _fetch_history(self, station_id: str, target_time: datetime) -> tuple[List[float], List[float], Optional[float]]:
        """
        Queries historical readings over past 24 hours to construct lag and rolling statistics.
        Returns: (hist_pm25, hist_aqi, prev_aqi_1h)
        """
        col = get_collection(Collections.NORMALIZED_ENVIRONMENT)
        if col is None:
            return [], [], None

        start_time = target_time - timedelta(hours=24)
        
        hist_pm25: List[float] = []
        hist_aqi: List[float] = []
        prev_aqi_1h: Optional[float] = None

        try:
            # Query chronological logs for station sorted by newest first
            cursor = col.find({
                "provider": "caaqms",
                "metadata.station_id": station_id,
                "timestamp": {"$gte": start_time, "$lt": target_time}
            }).sort("timestamp", -1)
            
            records = await cursor.to_list(length=100)
            
            for r in records:
                metrics = r.get("metrics", {})
                pm25_val = metrics.get("pm25")
                aqi_val = metrics.get("aqi")
                
                if pm25_val is not None:
                    hist_pm25.append(float(pm25_val))
                if aqi_val is not None:
                    hist_aqi.append(float(aqi_val))

            # Resolve 1h delta difference target (approx. 1 hour ago +/- 15 min window)
            delta_target = target_time - timedelta(hours=1)
            closest_1h_recs = [
                r for r in records
                if delta_target - timedelta(minutes=15) <= r["timestamp"] <= delta_target + timedelta(minutes=15)
            ]
            if closest_1h_recs:
                closest_1h = min(closest_1h_recs, key=lambda r: abs((r["timestamp"] - delta_target).total_seconds()))
                prev_aqi_1h = closest_1h.get("metrics", {}).get("aqi")
            elif records:
                # Fallback to the most recent record
                prev_aqi_1h = records[0].get("metrics", {}).get("aqi")

        except Exception as e:
            self.logger.warning(f"Error querying historical logs for station '{station_id}': {e}")

        return hist_pm25, hist_aqi, prev_aqi_1h
