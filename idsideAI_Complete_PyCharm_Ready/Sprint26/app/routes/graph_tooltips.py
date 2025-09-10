"""
Sprint 24.4 — Graph tooltip routes (protocol v2)
"""

from typing import Dict, Any
from fastapi import APIRouter, Body
from app.utils.graph_tooltips import add_tooltips

router = APIRouter(prefix="/api/graphs", tags=["graphs-tooltips"])


@router.post("/tooltips")
def tooltips(svg: str = Body(""), tooltips: Dict[str, Any] = Body(default={})):
    return {"svg": add_tooltips(svg, tooltips)}
