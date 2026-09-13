"""FastAPI application for the Options Backtester Web UI."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from web.backend.routers import backtest, data, instruments

app = FastAPI(title="Options Backtester", version="1.0.0")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000", "http://127.0.0.1:5173", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
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
