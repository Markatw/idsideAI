from typing import Annotated
"""
Analytics dashboard routes (Sprint 23.8, protocol v2)
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Body

from app.utils.analytics_dash import seed_dashboard, summarize

router = APIRouter(prefix="/api/analytics/dash", tags=["analytics-dash"])


@router.post("/summary")
def summary(events: Annotated[List[Dict[str, Any]] , Body(..., embed=True)]):
    return summarize(events)


@router.post("/seed")
def seed(events: Annotated[List[Dict[str, Any]] , Body(..., embed=True)]):
    return seed_dashboard(events)
