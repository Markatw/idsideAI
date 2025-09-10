"""
Sprint 26.7 — Probe routes (protocol v2)
"""

from fastapi import APIRouter, Query, Body
from app.utils import probe

router = APIRouter(prefix="/api/probe", tags=["probe"])


@router.get("/check")
def check(url: str = Query(...)):
    return probe.check_url(url)


@router.post("/batch")
def batch(urls: list[str] = Body(...)):
    return probe.uptime(urls)
