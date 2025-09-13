from typing import Annotated
"""
Sprint 26.7 — Probe routes (protocol v2)
"""

from fastapi import APIRouter, Body, Query

from app.utils import probe

router = APIRouter(prefix="/api/probe", tags=["probe"])


@router.get("/check")
def check(url: Annotated[str, Query(...)):
    return probe.check_url(url)


@router.post("/batch")
def batch(urls: Annotated[list[str], Body(...)):
    return probe.uptime(urls)
