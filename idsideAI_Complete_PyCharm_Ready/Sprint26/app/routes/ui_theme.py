"""
Sprint 24.5 — Theme endpoints (protocol v2)
"""
from typing import Any, Dict
from fastapi import APIRouter, Body
from app.utils.ui_theme import get_tokens, toggle_mode

router = APIRouter(prefix="/api/theme", tags=["theme"])

@router.post("/tokens")
def tokens(mode: str = Body("light")) -> Dict[str, Any]:
    return get_tokens(mode)

@router.post("/toggle")
def toggle(pref: str = Body("auto")) -> Dict[str, Any]:
    next_mode = toggle_mode(pref)
    return {"next_mode": next_mode, "tokens": get_tokens(next_mode if next_mode != "auto" else "light")}
