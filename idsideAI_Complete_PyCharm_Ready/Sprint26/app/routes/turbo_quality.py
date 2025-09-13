"""
Sprint 21.3 — Turbo quality monitoring API (protocol v2)
- POST /api/turbo/quality/classify  -> failure classification for a single event
- POST /api/turbo/quality/check     -> threshold checks for metric snapshot
Router wiring via include_router can be added separately to avoid startup coupling.
"""

from typing import Dict
from fastapi import APIRouter

router = APIRouter(prefix="/turbo-quality", tags=["turbo-quality"])

from ..utils.turbo_quality import check_thresholds

from typing import Annotated
from fastapi import Body  # (should already be there, keep it)

@router.post("/check")
def check(
    metrics: Annotated[Dict[str, float], Body(..., embed=True)],
    thresholds: Annotated[Dict[str, float], Body(..., embed=True)],
):

    return check_thresholds(metrics, thresholds)



@router.post("/check")
def check(
    metrics: Annotated[Dict[str, float], Body(..., embed=True)],
    thresholds: Annotated[Dict[str, float], Body(..., embed=True)],
):
    return {"alerts": check_thresholds(metrics, thresholds)}
