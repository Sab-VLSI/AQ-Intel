# System Architecture & Technical Design Reference

> **NAQMP Platform Software Architecture Specifications**

---

## 1. Domain Directory Hierarchy

```
src/
├── components/          # Design system primitives & shell layout
│   ├── auth/            # Auth layout wrappers
│   ├── layout/          # AppShell, Navigation, Header, Sidebar, Footer
│   └── ui/              # Button, Input, Select, Textarea, Modal, DataTable, FilterBar, etc.
├── config/              # Centralized route & endpoint registry (apiEndpoints.ts)
├── constants/           # AQI bands, pollutant limits, palette tokens
├── data/                # Seed domain datasets & mock reference objects
├── features/            # Feature modules (Domain Driven Design)
│   ├── admin/           # Administration workspace
│   ├── alerts/          # Alert management & command center
│   ├── analytics/       # Historical trends, reports, AI predictions
│   ├── auth/            # Login, password recovery, session lock
│   ├── help/            # Knowledge base, support tickets, feedback
│   ├── monitoring/      # Stations list, telemetry detail, station comparison, map
│   ├── operations/      # Tasks, inspections, AI recommendations
│   ├── overview/        # Command Center main dashboard
│   ├── settings/        # System settings & administrative sub-modules
│   └── workspace/       # User profile, personal tasks, notifications, preferences
├── hooks/               # Shared custom hooks (useDebounce, usePageTitle, usePagination)
├── routes/              # Application router & protected navigation guard
├── services/            # Service layer & API client (apiClient, authService, etc.)
├── stores/              # Global Zustand stores (useAuthStore, useUIStore, useSensorStore)
└── types/               # TypeScript domain DTOs (user, admin, report, support, etc.)
```

---

## 2. Service Layer & HTTP Abstraction

All REST backend calls flow through `apiClient.ts`:

- **Interceptors**: Injects `Authorization: Bearer <token>` into outgoing requests.
- **Auto-Refresh**: Intercepts `401 Unauthorized` responses to refresh tokens.
- **Error Classification**: Maps HTTP status codes to typed `APIError` codes (`UNAUTHORIZED`, `FORBIDDEN`, `VALIDATION_ERROR`, `SERVER_ERROR`).
- **Offline Fallback**: Supports `VITE_USE_MOCK_DATA` flag to return fallback objects during offline or staging runs.

```
Component ──► Feature Hook ──► Service Layer ──► apiClient ──► REST API
```

---

## 3. Global State Architecture

- **Auth State (`useAuthStore`)**: Authenticated user session, tokens, RBAC roles.
- **UI State (`useUIStore`)**: Active theme, sidebar collapse state, toast notifications stack.
- **Telemetry State (`useSensorStore`)**: Station filters, active station selection, map view settings.

---

## 4. UI/UX Design Token Specifications

- **Typography**: Inter / Outfit sans-serif font stack.
- **Color Tokens**:
  - Primary Accent: Sky (`#0284C7`, `bg-sky-600`)
  - Background: Clean Administrative Slate (`#F8FAFC`, `bg-slate-50`)
  - Borders: Subdued Slate (`#E2E8F0`, `border-slate-200`)
  - AQI Bands: Good (Green), Moderate (Yellow), Poor (Orange), Unhealthy (Red), Severe (Purple), Hazardous (Maroon).
