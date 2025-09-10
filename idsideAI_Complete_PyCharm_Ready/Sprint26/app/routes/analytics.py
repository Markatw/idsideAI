"""
Sprint 22.8 — Analytics API (protocol v2)
- POST /api/analytics/event {event: {...}} -> append
- GET  /api/analytics/events?limit=1000     -> list recent events
"""
from typing import Any, Dict
from fastapi import APIRouter, Body, Query
from app.utils.analytics import append_event, list_events

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.post("/event")
def add_event(event: Dict[str, Any] = Body(..., embed=True)):
    return append_event(event)

@router.get("/events")
def events(limit: int = Query(1000, ge=1, le=10000)):
    return {"events": list_events(limit)}
