from fastapi import Body
from typing import Annotated
"""
Sprint 24.4 — Graph tooltip routes (protocol v2)
"""

from typing import Any, Dict

from fastapi import APIRouter, Body

from app.utils.graph_tooltips import add_tooltips

router = APIRouter(prefix="/api/graphs", tags=["graphs-tooltips"])


@router.post("/tooltips")
def tooltips(svg: Annotated[str , Body("")], tooltips: Annotated[Dict[str, Any] , Body(default={})]):
    return {"svg": add_tooltips(svg, tooltips)}
