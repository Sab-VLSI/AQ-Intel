# 🌍 AQIntel – Urban Air Quality Intelligence Platform


<p align="center">
<b>AI-Powered Urban Air Quality Intelligence & Decision Support Platform</b>

Real-Time Air Quality Monitoring • Environmental Intelligence • AI Analytics • Decision Support
</p>

<p align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-4DB33D)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

# 📖 Overview

AQIntel is an AI-powered Urban Air Quality Intelligence Platform developed to help government agencies, pollution control boards, and smart cities monitor, analyze, forecast, and respond to urban air pollution in real time.

Unlike traditional AQI dashboards that simply visualize sensor readings, AQIntel combines multiple environmental data sources into a unified intelligence platform capable of generating operational insights, environmental risk assessments, and actionable recommendations.

The platform follows a **backend-first architecture**, where all calculations, intelligence generation, and decision support are performed on the backend while the frontend focuses solely on visualization.

---

# ✨ Features

## 🌫 Air Quality Monitoring

- Real-time AQI monitoring
- Multi-station monitoring
- City-wide AQI computation
- Historical air quality analysis
- Pollutant monitoring
- Live monitoring stations

---

## 🗺 Interactive Monitoring Map

- OpenStreetMap Integration
- Live AQI station markers
- Color-coded AQI visualization
- Wind direction indicators
- Interactive station popup
- Real-time monitoring

---

## 🌦 Weather Intelligence

- Temperature
- Humidity
- Wind Speed
- Wind Direction
- Atmospheric Conditions

---

## 🔥 Fire Intelligence

Integrated NASA FIRMS support

- Fire Hotspots
- Fire Radiative Power
- Fire Confidence
- Nearest Fire Source

---

## 🛣 Corridor Intelligence

- High-risk corridors
- AQI corridor ranking
- Diversion recommendations
- Environmental risk analysis
- Wind influence

---

## 🌱 Geospatial Intelligence

Powered by OpenStreetMap

- Road Density
- Green Cover
- Industrial Areas
- Residential Areas
- Commercial Areas
- Water Bodies
- Land-use Classification

---

## 📈 Forecasting

- AQI Prediction
- PM2.5 Prediction
- Pollution Trends
- Environmental Forecasting

---

## 🧠 AI Source Attribution

Estimate pollution contribution from

- Vehicular Emissions
- Industrial Activities
- Construction
- Biomass Burning
- Road Dust
- Domestic Sources

---

## 📄 AI Reports

Automatically generate

- Daily AQI Reports
- Enforcement Reports
- Environmental Summaries
- Decision Support Reports

---

# 🏗 System Architecture

```text
                    External Data Sources

   CPCB CAAQMS     Weather API     NASA FIRMS     OpenStreetMap
          │              │              │               │
          └──────────────┼──────────────┼───────────────┘
                         │
                         ▼
                 Provider Layer
                         │
                         ▼
             Validation & Normalization
                         │
                         ▼
                    MongoDB Storage
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 normalized_*    station_snapshot    historical_data
                         │
                         ▼
                Data Fusion Engine
                         │
                         ▼
              Intelligence Generation
                         │
     ┌─────────────┬────────────┬──────────────┐
     ▼             ▼            ▼              ▼
 Dashboard     Live AQI     Corridor AI     Reports
```

---

# 🛠 Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Zustand
- React Query
- Chart.js
- Leaflet

---

## Backend

- FastAPI
- Python
- Pydantic
- APScheduler
- AsyncIO

---

## Database

- MongoDB

---

## Mapping

- OpenStreetMap
- Overpass API
- Leaflet

---

## AI & Analytics

- Forecast Engine
- Data Fusion Engine
- Source Attribution Engine
- Recommendation Engine

---

# 📂 Project Structure

```text
AQIntel/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── providers/
│   │   ├── services/
│   │   ├── agents/
│   │   ├── scheduler/
│   │   ├── database/
│   │   ├── models/
│   │   ├── utils/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── features/
│   │   ├── repositories/
│   │   ├── stores/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── config/
│   │
│   └── package.json
│
├── docs/
├── assets/
└── README.md
```

---

# 🔄 Data Pipeline

```text
Live APIs
     │
     ▼
Validation
     │
     ▼
Normalization
     │
     ▼
MongoDB
     │
     ▼
Station Snapshot
     │
     ▼
Data Fusion Engine
     │
     ▼
AI Intelligence
     │
     ▼
Dashboard
```

---

# 📊 Backend Modules

| Module | Description |
|----------|-------------|
| CAAQMS Provider | CPCB Air Quality Data |
| Weather Provider | Weather Intelligence |
| NASA FIRMS | Fire Monitoring |
| OSM Provider | Geographic Intelligence |
| Validation Engine | Data Validation |
| Normalization Engine | Unified Data Schema |
| Data Fusion Engine | Multi-source Integration |
| Forecast Engine | AQI Prediction |
| Source Attribution | Pollution Source Analysis |
| Scheduler | Automatic Data Refresh |

---

# 🗄 MongoDB Collections

| Collection | Purpose |
|------------|----------|
| normalized_environment | Historical AQI observations |
| normalized_weather | Weather observations |
| normalized_fire | Fire hotspot data |
| normalized_osm | Geographic intelligence |
| station_snapshot | Latest station observations |
| corridor_snapshot | Corridor intelligence |

---

# 🌐 API Overview

## Dashboard

```http
GET /api/v1/dashboard/summary
```

Returns

- City AQI
- Health
- Weather
- Forecast
- Alerts
- Trend

---

## Live Monitoring

```http
GET /api/v1/map/stations
```

Returns

- Live AQI stations
- Coordinates
- AQI
- Weather
- Status

---

## Station Telemetry

```http
GET /api/v1/stations

GET /api/v1/stations/{station_id}

GET /api/v1/stations/{station_id}/history
```

---

## Corridor Intelligence

```http
GET /api/v1/corridors
```

Returns

- Corridor Ranking
- Risk Score
- Diversion Recommendation

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/your-username/AQIntel.git

cd AQIntel
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt

uvicorn backend.app.main:app --reload
```

Backend runs at

```
http://localhost:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# ⚙ Environment Variables

Create a `.env` file inside the backend directory.

```env
MONGODB_URI=your_mongodb_uri

DATABASE_NAME=aqintel

CPCB_API_KEY=xxxxxxxxxxxxxxxx

NASA_FIRMS_API_KEY=xxxxxxxxxxxxxxxx

WEATHER_API_KEY=xxxxxxxxxxxxxxxx
```

---

# 🎯 Design Principles

- Backend-driven architecture
- No frontend business logic
- No hardcoded values
- MongoDB as the single source of truth
- Modular and scalable services
- Real-time operational intelligence

---

# 🛣 Roadmap

- ✅ Live AQI Monitoring
- ✅ OSM Integration
- ✅ Weather Intelligence
- ✅ Fire Intelligence
- ✅ Dashboard
- 🚧 Corridor Intelligence
- 🚧 Data Fusion Engine
- 🚧 Forecast Engine
- 🚧 Source Attribution
- 🚧 AI Reports
- 🚧 Decision Support
- 🚧 Mobile Application

---

# 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push the branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Developed By

**AQIntel Development Team**

*Building AI-powered Urban Air Quality Intelligence for smarter, cleaner, and data-driven cities.*

*Tried our maximum within 1 week due to college's exam constraints*
