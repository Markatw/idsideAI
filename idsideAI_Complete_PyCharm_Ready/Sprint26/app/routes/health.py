"""
Sprint 27.5 — Healthcheck endpoints (protocol v2)
"""
import os
from fastapi import APIRouter
from app.utils import metrics

router = APIRouter(tags=["health"])

@router.get("/healthz")
def liveness():
    # dumb increment to keep counters visible
    try:
        metrics.inc_counter("healthz")
    except Exception:
        pass
    return {"ok": True, "status": "alive"}

@router.get("/readyz")
def readiness():
    # minimal readiness: env wiring present, optionally ping dependencies in future
    deps = {
        "database_url_present": bool(os.getenv("DATABASE_URL")),
        "redis_url_present": bool(os.getenv("REDIS_URL")),
    }
    ready = True  # default to ready when not running in docker-compose with real deps
    return {"ok": ready, "deps": deps}
