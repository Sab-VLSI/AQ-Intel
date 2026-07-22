# AQIntel Decision Impact Simulator Report

Generated At: `2026-07-16T10:53:24.257605`

## Current Environmental State
- **AQI**: 185.0
- **PM2.5**: 88.0
- **City**: Chennai

## Simulation Results — Ranked by Recommendation Score

| Rank | Intervention | Category | Expected ΔAQl | Confidence | Cost | Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Heavy Vehicle Diversion | Traffic | -0.0 | MEDIUM | Low | 0.5000 |
| 2 | Peak-Hour Traffic Restriction | Traffic | -0.0 | MEDIUM | Low | 0.5000 |
| 3 | Construction Dust Suppression | Construction | -0.0 | MEDIUM | Low | 0.5000 |
| 4 | Industrial Stack Monitoring | Industrial | -0.0 | MEDIUM | Low | 0.5000 |
| 5 | Biomass Burning Prohibition | Biomass | -0.0 | MEDIUM | Low | 0.5000 |
| 6 | Street Washing | Environment | -0.0 | MEDIUM | Low | 0.5000 |
| 7 | Industrial Emission Reduction | Industrial | -1.1 | MEDIUM | Medium | 0.4563 |
| 8 | Alternate Traffic Routing | Traffic | -0.0 | MEDIUM | Medium | 0.4475 |
| 9 | Construction Work-Hour Restriction | Construction | -0.0 | MEDIUM | Medium | 0.4475 |
| 10 | Biomass Waste Collection | Biomass | -0.0 | MEDIUM | Medium | 0.4475 |
| 11 | Construction Temporary Suspension | Construction | -0.0 | MEDIUM | High | 0.4025 |
| 12 | Green Barrier Deployment | Environment | -0.0 | MEDIUM | High | 0.4025 |

## Top Recommendation Details
**Heavy Vehicle Diversion**

> Heavy Vehicle Diversion is recommended because Mixed / Unknown is the dominant source (26.8% confidence). Simulation projects an AQI reduction of ~minimal points. 5 similar past event(s) support this action. Overall simulation confidence: MEDIUM.

### Key Feature Changes
| Feature | Before | After | Delta |
| :--- | :--- | :--- | :--- |
| traffic_density | 0.85 | 0.68 | -0.17 |
| road_density | 0.7 | 0.63 | -0.07 |

### SHAP Explanation (Before → After)
| Feature | SHAP Before | SHAP After | SHAP Delta |
| :--- | :--- | :--- | :--- |
| traffic_density_score | 0.0027 | 0.0027 | 0.0 |
| pm25 | 0.0 | 0.0 | 0.0 |
| nearest_fire_bearing | 0.01 | 0.01 | 0.0 |
| co | 0.2615 | 0.2615 | 0.0 |
| humidity | 0.0 | 0.0 | 0.0 |

### Supporting Historical Evidence
- **Chennai** — Action: _None_ — Outcome: None — Similarity: 0.50
- **Chennai** — Action: _Odd-Even Scheme_ — Outcome: Improved — Similarity: 0.45
- **Chennai** — Action: _Odd-Even Traffic Scheme_ — Outcome: Improved — Similarity: 0.43