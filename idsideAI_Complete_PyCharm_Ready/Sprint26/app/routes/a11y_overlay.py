from typing import Annotated
"""
Sprint 24.7 — Accessibility overlay routes (protocol v2)
"""

from typing import Any, Dict

from fastapi import APIRouter, Body

from app.utils.a11y_overlay import scan_page

router = APIRouter(prefix="/api/a11y", tags=["a11y-overlay"])


@router.post("/scan")
def scan(html: Annotated[str, Body("")) -> Dict[str, Any]:
    return scan_page(html)
