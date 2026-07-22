# AQIntel Coordinator Execution Report

Generated At: `2026-07-16T11:39:33.384303`
Pipeline Version: `1.0.0`
Overall Decision Confidence: **MEDIUM**

## 1. Input Observation
- **City**: Chennai
- **Ward**: Central
- **Coordinates**: (13.0827, 80.2707)

## 2. Policy Action Recommendations

| ID | Policy Recommendation | Category | Expected ΔAQI | Priority | Cost |
| :--- | :--- | :--- | :--- | :--- | :--- |
| REC-202607161139-00 | Heavy Vehicle Diversion | Traffic | -0.0 | Medium | Low |
| REC-202607161139-01 | Peak-Hour Traffic Restriction | Traffic | -0.0 | Medium | Low |
| REC-202607161139-02 | Construction Dust Suppression | Construction | -0.0 | Medium | Low |

### Top Recommendation Rationale
> Heavy Vehicle Diversion is recommended because Mixed / Unknown is the dominant source (26.8% confidence). Simulation projects an AQI reduction of ~minimal points. 5 similar past event(s) support this action. Overall simulation confidence: MEDIUM.

## 3. Pipeline Timing Metrics
- **Feature Engineering**: `0.0 ms`
- **Source Attribution**: `31.0 ms`
- **Forecasting**: `15.0 ms`
- **Urban Memory Retrieval**: `0.0 ms`
- **Decision Simulation**: `266.0 ms`
- **Total End-to-End Pipeline**: **`312.0 ms`**

## 4. Warnings and Fallbacks Logs
- [!] Forecast missing estimated target: 'aqi'
- [!] Forecast missing estimated target: 'pm25'
- [!] Forecast results missing or invalid 'top_drivers' list.