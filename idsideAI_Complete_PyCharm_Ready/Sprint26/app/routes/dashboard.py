from typing import Annotated
"""
Sprint 24.3 — Dashboard routes (protocol v2)
"""

from typing import Any, Dict, List

from fastapi import APIRouter, Body, Query

from app.utils.ui_dashboard import layout, validate_tiles

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.post("/layout")
def get_layout(
    tiles: Annotated[List[Dict[str, Any]] , Body(default=[])], width: int = Query(1200)
):
    return {"layout": layout(tiles, width), "cols": None}


@router.post("/validate")
def validate(tiles: Annotated[List[Dict[str, Any]] , Body(default=[])]):
    return validate_tiles(tiles)
