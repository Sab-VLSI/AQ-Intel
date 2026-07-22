"""
AQIntel FastAPI application entry point.
Binds routers, registers lifecycle startup/shutdown events, and sets up middleware.
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

import logging
import time
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.logging import start_logging, stop_logging, get_logger
from backend.app.core.database import db_manager

# Import API Routers
from backend.app.api.routes.system import router as system_router
from backend.app.api.routes.analysis import router as analysis_router
from backend.app.api.routes.orchestration import router as orchestration_router
from backend.app.api.routes.map import router as map_router
from backend.app.api.routes.fusion import router as fusion_router
from backend.app.api.routes.dashboard_summary import router as dashboard_summary_router
from backend.app.api.routes.corridors import router as corridors_router
from backend.app.api.routes.priorities import router as priorities_router

# Import background job scheduler
from backend.app.scheduler import start_scheduler, stop_scheduler

# Import Telegram Bot client
from backend.app.telegram import TelegramBotClient

# ── Bootstrap logging FIRST (before any other import that might log) ──
start_logging()
logger = get_logger("aqintel.app")

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    description="AQIntel - AI-Powered Urban Air Quality Decision Intelligence Platform Backend",
    version=settings.APP_VERSION,
    # Configure Swagger UI & Redoc under versioned path
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json",
    docs_url=f"/api/{settings.API_VERSION}/docs",
    redoc_url=f"/api/{settings.API_VERSION}/redoc",
)

# Apply CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply Request Logging Middleware (BEFORE CORS so all requests are traced)
from backend.app.core.middleware import RequestLoggingMiddleware
app.add_middleware(RequestLoggingMiddleware)

# Instantiate the global Telegram Bot client daemon
bot_client = TelegramBotClient()

# Startup DB client and background tasks scheduler
@app.on_event("startup")
async def startup_db_client():
    t_start = __import__('time').perf_counter()
    logger.info("Starting up AQIntel backend app...")

    # Emit audit record and environment snapshot
    from backend.app.core.audit import audit
    from backend.app.core.health_monitor import log_startup_environment
    audit.startup(version=settings.APP_VERSION, extra={"environment": settings.ENVIRONMENT})
    log_startup_environment()

    db_manager.connect(settings.MONGODB_URI, settings.DATABASE_NAME)
    start_scheduler()
    await bot_client.start()

    # Pre-warm spatial grid cache for default city if enabled
    if settings.ENABLE_GRID_CACHE:
        logger.info(f"Pre-warming spatial grid cache for {settings.CITY_NAME}...")
        try:
            from backend.app.ml.spatial.grid_generator import AdaptiveGridGenerator
            grid_gen = AdaptiveGridGenerator(city_name=settings.CITY_NAME)
            grid_gen.generate_grid()
            logger.info("Successfully pre-warmed spatial grid cache.")
        except Exception as e:
            logger.warning(f"Failed to pre-warm spatial grid cache: {e}")

    # Launch heatmap precomputation in the background
    from backend.app.services.geospatial_service import precompute_and_store_heatmaps, refresh_station_snapshot
    asyncio.create_task(precompute_and_store_heatmaps())
    asyncio.create_task(refresh_station_snapshot())

    # Seed corridor snapshots on startup
    from backend.app.services.corridor_service import refresh_corridor_snapshots
    asyncio.create_task(refresh_corridor_snapshots())

    # Seed priority snapshots on startup
    from backend.app.services.priority_service import refresh_priority_snapshots
    asyncio.create_task(refresh_priority_snapshots())

    # Run scientific integrity audit asynchronously in background
    from backend.app.services.integrity_audit import run_scientific_integrity_audit
    asyncio.create_task(run_scientific_integrity_audit())

    startup_ms = round((__import__('time').perf_counter() - t_start) * 1000, 1)
    logger.info(f"AQIntel startup complete", extra={"x_startup_ms": startup_ms})

# Shutdown DB client and scheduler
@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down AQIntel backend app...")
    from backend.app.core.audit import audit
    audit.shutdown()
    db_manager.disconnect()
    stop_scheduler()
    bot_client.stop()
    stop_logging()  # Flush async queue and stop background logger thread

from backend.app.api.routes.stations import router as stations_router

# Register versioned routers
app.include_router(system_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(analysis_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(orchestration_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(map_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(fusion_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(dashboard_summary_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(stations_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(corridors_router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(priorities_router, prefix=f"/api/{settings.API_VERSION}")

# Register root /health shortcut for direct health status access
app.include_router(system_router)

# Add a simple redirect/welcome response on root index
@app.get("/", tags=["Index"])
async def read_index():
    return {
        "message": f"Welcome to the {settings.APP_NAME} APIs",
        "docs": f"/api/{settings.API_VERSION}/docs",
        "health": f"/api/{settings.API_VERSION}/health"
    }
