# National Air Quality Monitoring Platform (NAQMP)

> **Production Release Version 3.0** — Government Air Quality Monitoring & Emergency Decision Support System.

![Build Status](https://img.shields.io/badge/Build-Passing-emerald)
![React](https://img.shields.io/badge/React-19.2-sky)
![TypeScript](https://img.shields.io/badge/TypeScript-Strict-blue)
![Tailwind](https://img.shields.io/badge/Tailwind-v4-purple)
![Vite](https://img.shields.io/badge/Vite-8.1-amber)

---

## 🏛️ Executive Summary

The **National Air Quality Monitoring Platform (NAQMP)** is an enterprise decision-support application built for central and regional environmental control boards (e.g., CPCB / SPCB). It delivers real-time air quality index (AQI) telemetry, AI-driven emissions forecasting, automated emergency alert dispatches, field inspection dockets, administrative governance, and compliance reporting.

---

## 🚀 Key Features & Functional Modules

1. **Command Center Dashboard (`/`)**:
   - City-wide average AQI telemetry and status metrics.
   - Priority incident panel & emergency dispatch shortcuts.
   - 24-hour pollutant trend chart and GIS district map preview.

2. **Monitoring Module (`/monitoring/*`)**:
   - Live telemetry grid covering registered monitoring stations.
   - Individual station detail view (`/monitoring/stations/:id`) with multi-pollutant breakdown (PM2.5, PM10, CO2, NO2, O3, SO2).
   - Side-by-side station comparison (`/monitoring/compare`).
   - GIS interactive map (`/monitoring/map`).

3. **Operations Module (`/operations/*`)**:
   - Field officer task dockets (`/operations/tasks`).
   - Facility compliance inspection schedules (`/operations/inspections`).
   - AI-generated mitigation recommendations (`/operations/recommendations`).

4. **Analytics & AI Forecasting (`/analytics/*`)**:
   - Multi-district trend comparison (`/analytics/trends`).
   - AI predictive scenario simulator (`/analytics/predictions`).
   - Compliance report generator (`/analytics/reports`).

5. **Administration Module (`/administration/*`)**:
   - User account directory, roles, and department registries (`/administration/users`).
   - System settings, alert threshold configurations, and backup management (`/administration/system`).
   - Immutable security audit logs (`/administration/audit-logs`).

6. **User Workspace (`/workspace/*`)**:
   - User profile details, security credential updates, personal tasks, and notification feeds.
   - Support ticket submit & chat messaging center (`/help`).

---

## 🛠️ Technology Stack

- **Framework**: React 19 + TypeScript (Strict compiler mode)
- **Bundler**: Vite 8 with manual vendor chunking and Terser minification
- **Styling**: Vanilla CSS + Tailwind CSS v4 + Lucide React Icons
- **State Management**: Zustand stores + React Context
- **Form Validation**: React Hook Form + Zod
- **Data Visualization**: Recharts time-series charts
- **Animation**: Framer Motion
- **Containerization**: Docker + Multi-stage Nginx Alpine builder

---

## 💻 Quick Start & Development Setup

### Prerequisites
- Node.js >= 20.0.0
- npm >= 10.0.0

### Installation

```bash
# Clone repository
git clone https://github.com/cpcb/naqmp-frontend.git
cd naqmp-frontend

# Install dependencies
npm install

# Start Vite local development server
npm run dev
```

The application will be accessible at `http://localhost:5173`.

---

## 📦 Production Build & Testing

```bash
# Execute TypeScript strict check and Vite production build
npm run build

# Preview production build locally
npm run preview
```

---

## 🐳 Docker Deployment

```bash
# Build and launch production Docker container on port 80
docker-compose up --build -d
```

---

## 📄 License & Attribution

Internal Government Software — National Air Quality Monitoring Platform (NAQMP). Authorized use only.
