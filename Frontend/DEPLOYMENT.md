# Production Deployment & Operational Handbook

> **NAQMP Enterprise Release 3.0 Deployment Specification**

---

## 1. Production Architecture Overview

The frontend application compiles into static JavaScript, CSS, and HTML bundles optimized for high-availability distribution via CDN or Nginx web servers.

```
┌─────────────────────────────────────────────────────────────┐
│                      Nginx Web Server                       │
│     (Listens on Port 80/443 with HSTS, CSP, and Gzip)       │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌──────────────────────┐               ┌──────────────────────┐
│  Static Web Assets   │               │   REST API Gateway   │
│  (React 19 Bundle)   │               │(https://api.naqmp.gov)│
└──────────────────────┘               └──────────────────────┘
```

---

## 2. Environment Variables

Create `.env` in the root directory prior to building for production:

| Variable | Required | Description | Example |
|---|---|---|---|
| `VITE_APP_ENV` | Yes | Target deployment environment | `production` |
| `VITE_API_URL` | Yes | Microservices API Gateway endpoint | `https://api.naqmp.gov.in/v1` |
| `VITE_API_TIMEOUT` | No | Request timeout in milliseconds | `10000` |
| `VITE_API_VERSION` | No | API release version tag | `v1` |
| `VITE_USE_MOCK_DATA` | Yes | Sandbox mode flag (set `false` in production) | `false` |

---

## 3. Docker Deployment Instructions

### Build Docker Image Manually

```bash
docker build -t naqmp-frontend:v3.0 .
docker run -d -p 80:80 --name naqmp-app naqmp-frontend:v3.0
```

### Orchestrate via Docker Compose

```bash
# Launch containerized web server in background
docker-compose up -d --build

# Verify container health
docker-compose ps
```

---

## 4. Bare-Metal Nginx Configuration

If deploying directly to Linux servers (Ubuntu/RHEL) with Nginx:

1. Build static assets: `npm run build`
2. Copy `dist/*` files to `/var/www/naqmp/html/`
3. Symlink `nginx.conf` to `/etc/nginx/conf.d/naqmp.conf`
4. Test configuration and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 5. Security & HTTP Headers

The production Nginx configuration automatically enforces:

- **Content-Security-Policy (CSP)**: Restricts script, style, and API origins.
- **X-Frame-Options**: `DENY` (prevents clickjacking attacks).
- **X-Content-Type-Options**: `nosniff` (prevents MIME sniffing).
- **X-XSS-Protection**: `1; mode=block`.
- **HSTS / TLS 1.3 Readiness**.

---

## 6. Health Checks & Monitoring

- **Synthetic Health Endpoint**: `GET http://<server-ip>/healthz` (Returns `200 OK`).
- **Nginx Error Logs**: `/var/log/nginx/error.log`.
