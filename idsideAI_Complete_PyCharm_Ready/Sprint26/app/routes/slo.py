"""
Sprint 26.6 — SLO routes (protocol v2)
"""

from fastapi import APIRouter, Body
from app.utils import slo

router = APIRouter(prefix="/api/slo", tags=["slo"])


@router.post("/record")
def record(success: bool = Body(...)):
    slo.record(success)
    return {"ok": True}


@router.get("/status")
def get_status():
    return slo.status()
