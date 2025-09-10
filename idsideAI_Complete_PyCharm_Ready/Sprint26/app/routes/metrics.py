"""
Sprint 25.7 — Metrics routes (protocol v2)
"""

from typing import Any, Dict
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import time
from app.utils.metrics import inc_counter, observe_latency, render_prometheus

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("/health")
def health() -> Dict[str, Any]:
    inc_counter("app_health_checks_total", 1)
    return {"ok": True}


@router.get("/probe")
def probe() -> Dict[str, Any]:
    t0 = time.perf_counter()
    # simulate small work
    for _ in range(1000):
        pass
    dt = time.perf_counter() - t0
    observe_latency("app_request_latency_seconds", dt)
    inc_counter("app_requests_total", 1)
    return {"ok": True, "latency_seconds": dt}


@router.get("/prometheus", response_class=PlainTextResponse)
def prometheus():
    return render_prometheus()
