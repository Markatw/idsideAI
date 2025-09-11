"""
Sprint 21.3 — Turbo quality monitoring API (protocol v2)
- POST /api/turbo/quality/classify  -> failure classification for a single event
- POST /api/turbo/quality/check     -> threshold checks for metric snapshot
Router wiring via include_router can be added separately to avoid startup coupling.
"""

from typing import Any, Dict

from fastapi import APIRouter, Body

from app.utils.turbo_quality import check_thresholds, classify_failure

router = APIRouter(prefix="/api/turbo/quality", tags=["turbo_quality"])


@router.post("/classify")
def classify(event: Dict[str, Any] = Body(..., embed=True)):
    return classify_failure(event)


@router.post("/check")
def check(
    metrics: Dict[str, float] = Body(..., embed=True),
    thresholds: Dict[str, float] = Body(..., embed=True),
):
    return {"alerts": check_thresholds(metrics, thresholds)}
