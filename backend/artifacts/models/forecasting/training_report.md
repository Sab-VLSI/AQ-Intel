# AQIntel Forecasting Model Training Execution Report

Generated At: `2026-07-22T07:15:45.712812`

## 1. Metadata Details
- **Model Version**: `1.0.0`
- **Feature Version**: `1.0.0`
- **Total Training Records**: 200

## 2. Selected Feature List
Selected features: `aqi, aqi_lag_12h, aqi_lag_1h, aqi_lag_24h, aqi_rolling_mean_24h, aqi_rolling_mean_6h, aqi_rolling_std_24h, average_frp, co, construction_score, fire_count, green_cover, heavy_vehicle_score, humidity, industrial_distance, maximum_frp, nearest_fire_distance, nh3, no2, o3, pm10, pm25, pm25_lag_12h, pm25_lag_1h, pm25_lag_24h, pm25_rolling_mean_24h, pm25_rolling_mean_6h, pm25_rolling_std_24h, precipitation, pressure, road_congestion_score, road_density, so2, temperature, traffic_density_score, water_distance, wind_direction, wind_speed`

## 3. Evaluation Performance Metrics on Test Set

### Target Variable: `AQI`
- **MAE**: 16.7706
- **RMSE**: 22.5511
- **R² Score**: 0.0230

### Target Variable: `PM25`
- **MAE**: 23.0887
- **RMSE**: 25.8170
- **R² Score**: -0.1891
