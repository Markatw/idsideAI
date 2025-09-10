"""
Sprint 22.2 — Telemetry API (protocol v2)
- POST /api/telemetry/export -> CSV export
- POST /api/telemetry/summary -> summary stats
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Body
from app.utils.telemetry_export import export_events_csv, summarize_events

router = APIRouter(prefix="/api/telemetry", tags=["telemetry"])


@router.post("/export")
def export(events: List[Dict[str, Any]] = Body(..., embed=True)):
    return {"csv": export_events_csv(events)}


@router.post("/summary")
def summary(events: List[Dict[str, Any]] = Body(..., embed=True)):
    return summarize_events(events)


@router.get("/summary")
def summary_get():
    # This GET returns an empty-summary schema for now (no server-held buffer here).
    # Clients that have events should use POST /summary with an events body.
    return {
        "total_events": 0,
        "avg_latency_ms": 0,
        "failures": 0,
        "failure_rate": 0.0,
        "providers_used": [],
    }
