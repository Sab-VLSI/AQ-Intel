"""
AQIntel constants.
Centralized repository for constants, collection names, and configuration limits.
"""

from typing import Dict, List, Set

# Supported Data Providers
SUPPORTED_PROVIDERS: Set[str] = {
    "CAAQMS",
    "OpenWeather",
    "OpenStreetMap",
    "NASA_FIRMS",
    "ActivitySim"
}

# Pollutants defined by standards (CPCB/EPA)
POLLUTANTS: List[str] = [
    "pm25",
    "pm10",
    "no2",
    "so2",
    "co",
    "o3",
    "nh3"
]

# AQI Categories (CPCB standard)
AQI_CATEGORIES: Dict[str, Dict[str, int]] = {
    "Good": {"min": 0, "max": 50},
    "Satisfactory": {"min": 51, "max": 100},
    "Moderate": {"min": 101, "max": 200},
    "Poor": {"min": 201, "max": 300},
    "Very Poor": {"min": 301, "max": 400},
    "Severe": {"min": 401, "max": 500}
}

# Database Collection Names (to prevent string typos across modules)
class Collections:
    RAW_WEATHER = "raw_weather"
    RAW_CAAQMS = "raw_caaqms"
    RAW_FIRE = "raw_fire"
    RAW_OSM = "raw_osm"
    NORMALIZED_ENVIRONMENT = "normalized_environment"
    NORMALIZED_WEATHER = "normalized_weather"
    NORMALIZED_FIRE = "normalized_fire"
    NORMALIZED_OSM = "normalized_osm"
    FUSED_ENVIRONMENT = "fused_environment"
    FEATURE_STORE = "feature_store"
    FEATURE_HISTORY = "feature_history"
    STATION_SNAPSHOT = "station_snapshot"
    CORRIDOR_SNAPSHOT = "corridor_snapshot"
    PRIORITY_SNAPSHOT = "priority_snapshot"

# Geographical defaults
DEFAULT_CITY: str = "Chennai"
DEFAULT_COUNTRY: str = "India"
DEFAULT_TIMEZONE: str = "Asia/Kolkata"
DEFAULT_LATITUDE: float = 13.0827
DEFAULT_LONGITUDE: float = 80.2707
DEFAULT_RADIUS_METERS: int = 5000  # Default 5km search radius
