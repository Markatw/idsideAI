"""
Sprint 24.7 — Accessibility overlay routes (protocol v2)
"""

from fastapi import APIRouter, Body
from typing import Any, Dict
from app.utils.a11y_overlay import scan_page

router = APIRouter(prefix="/api/a11y", tags=["a11y-overlay"])


@router.post("/scan")
def scan(html: str = Body("")) -> Dict[str, Any]:
    return scan_page(html)
