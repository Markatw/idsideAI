"""
Analytics dashboard routes (Sprint 23.8, protocol v2)
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Body
from app.utils.analytics_dash import summarize, seed_dashboard

router = APIRouter(prefix="/api/analytics/dash", tags=["analytics-dash"])


@router.post("/summary")
def summary(events: List[Dict[str, Any]] = Body(..., embed=True)):
    return summarize(events)


@router.post("/seed")
def seed(events: List[Dict[str, Any]] = Body(..., embed=True)):
    return seed_dashboard(events)
