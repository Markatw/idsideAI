"""
Sprint 24.8 — Error routes (protocol v2)
"""

from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from app.utils.ui_errors import load_error_page

router = APIRouter(prefix="/api/errors", tags=["errors"])


@router.get("/page", response_class=HTMLResponse)
def page(code: int = Query(404)) -> str:
    return load_error_page(code)
