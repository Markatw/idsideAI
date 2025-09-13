from typing import Annotated
"""
Sprint 26.5 — Soak control routes (protocol v2)
"""

from fastapi import APIRouter, Body

from app.utils import soak

router = APIRouter(prefix="/api/soak", tags=["soak"])


@router.post("/start")
def start(interval: Annotated[int, Body(60), url: Annotated[str, Body(None)):
    ok = soak.start(interval, url)
    return {"started": ok}


@router.post("/stop")
def stop():
    soak.stop()
    return {"stopped": True}


@router.get("/status")
def status():
    return soak.status()
