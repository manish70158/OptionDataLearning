"""FastAPI application for the Options Backtester Web UI."""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from web.backend.auth import BasicAuthMiddleware
from web.backend.routers import auth, backtest, data, instruments

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """On startup, if there's a persisted Upstox token in the DB, load it
    into the shared pricing fetcher so cold-boot requests don't 401."""
    try:
        from web.backend.data.cache import init_db
        from web.backend.engine.pricing import _get_fetcher
        await init_db()
        fetcher = await _get_fetcher()
        loaded = await fetcher.reload_access_token()
        if loaded:
            logger.info("Loaded Upstox access token from DB on startup.")
    except Exception as e:
        logger.warning(f"Startup Upstox token load failed: {e}")
    yield


app = FastAPI(title="Options Backtester", version="1.0.0", lifespan=lifespan)

# Basic-auth gate for deployed environments (no-op when WEB_AUTH_USER/PASS are unset).
app.add_middleware(BasicAuthMiddleware)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000", "http://127.0.0.1:5173", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(auth.router, prefix="/api")
app.include_router(backtest.router, prefix="/api")
app.include_router(data.router, prefix="/api")
app.include_router(instruments.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


# Serve frontend static files in production
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
