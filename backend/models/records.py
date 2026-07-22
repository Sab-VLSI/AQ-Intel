"""
MongoDB Collection Document Models.
These models describe the structural layout of records stored in MongoDB collections.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import Field
from backend.app.models.base import MongoBaseModel
from backend.app.schemas.environment import Metrics, RecordMetadata
from backend.app.schemas.features import FeatureVector

class AQDocument(MongoBaseModel):
    """
    MongoDB document structure for Air Quality records.
    Stored in 'aq_records' collection.
    """
    station_id: str = Field(..., index=True)
    timestamp: datetime = Field(..., index=True)
    aqi: Optional[float] = None
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None
    o3: Optional[float] = None
    nh3: Optional[float] = None
    latitude: float
    longitude: float
    provider: str = Field(default="CAAQMS")

class WeatherDocument(MongoBaseModel):
    """
    MongoDB document structure for Weather records.
    Stored in 'weather_records' collection.
    """
    timestamp: datetime = Field(..., index=True)
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: float
    precipitation: float
    pressure: float
    latitude: float
    longitude: float

class GISDocument(MongoBaseModel):
    """
    MongoDB document structure for static and dynamic GIS attributes.
    Stored in 'gis_records' collection.
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    road_density: float
    industrial_distance: float
    land_use: str
    nearest_highway: str

class FireDocument(MongoBaseModel):
    """
    MongoDB document structure for active and thermal fire spots.
    Stored in 'fire_records' collection.
    """
    fire_id: str = Field(..., index=True)
    timestamp: datetime = Field(..., index=True)
    latitude: float
    longitude: float
    frp: float
    confidence: float
    type: str
    distance_to_city: float
    distance_to_station: float

class ActivityDocument(MongoBaseModel):
    """
    MongoDB document structure for urban activity indices.
    Stored in 'activity_records' collection.
    """
    timestamp: datetime = Field(..., index=True)
    latitude: float
    longitude: float
    traffic_density_score: float
    heavy_vehicle_score: float
    construction_score: float
    road_congestion_score: float

class EnvironmentDocument(MongoBaseModel):
    """
    MongoDB document structure for unified Environment records.
    Stored in 'normalized_environment' collection.
    """
    provider: str = Field(..., index=True)
    timestamp: datetime = Field(..., index=True)
    location: Dict[str, float] = Field(..., description="Coordinates e.g. {'latitude': 13.0827, 'longitude': 80.2707}")
    metrics: Metrics
    metadata: RecordMetadata

class FeatureStoreDocument(MongoBaseModel, FeatureVector):
    """
    MongoDB document mapping for feature_store records.
    """
    pass

class FeatureHistoryDocument(MongoBaseModel, FeatureVector):
    """
    MongoDB document mapping for feature_history records.
    """
    pass
