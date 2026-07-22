# AQIntel Attribution Model Training Execution Report

Generated At: `2026-07-22T07:15:59.219138`

## 1. Metadata Details
- **Model Version**: `1.0.0`
- **Feature Version**: `1.0.0`
- **Total Training Records**: 200
- **Dataset Fingerprint**: `61409c8e523ac5bef064850ebdab444d`

## 2. Selected Feature List
Selected features: `average_frp, co, construction_score, fire_count, green_cover, heavy_vehicle_score, humidity, industrial_distance, maximum_frp, nearest_fire_bearing, nearest_fire_distance, nh3, no2, o3, pm10, pm25, precipitation, pressure, road_congestion_score, road_density, so2, station_distance, temperature, traffic_density_score, water_distance, wind_direction, wind_speed`

## 3. Class Balance Distribution
| Category | Count |
| :--- | :--- |
| Industrial | 45 |
| Mixed / Unknown | 43 |
| Construction | 41 |
| Biomass Burning | 40 |
| Traffic | 31 |

## 4. Evaluation Performance Metrics on Test Set
- **Accuracy**: 0.3200
- **Precision (Weighted)**: 0.3217
- **Recall (Weighted)**: 0.3200
- **F1 Score (Weighted)**: 0.3204

## 5. Confusion Matrix
```json
[
  [
    2,
    1,
    1,
    1,
    2
  ],
  [
    0,
    2,
    0,
    4,
    1
  ],
  [
    1,
    0,
    2,
    2,
    3
  ],
  [
    4,
    1,
    3,
    5,
    2
  ],
  [
    1,
    2,
    2,
    3,
    5
  ]
]
```