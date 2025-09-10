"""
Sprint 24.6 — i18n endpoints (protocol v2)
"""

from typing import Any, Dict, List
from fastapi import APIRouter, Body, Query
from app.utils.i18n import set_lang, get_lang, t

router = APIRouter(prefix="/api/i18n", tags=["i18n"])


@router.post("/set")
def set_language(lang: str = Body("en")) -> Dict[str, Any]:
    return {"lang": set_lang(lang)}


@router.get("/get")
def get_language() -> Dict[str, Any]:
    return {"lang": get_lang()}


@router.post("/t")
def translate(
    keys: List[str] = Body(default=[]), lang: str = Query(None)
) -> Dict[str, Any]:
    return {"lang": lang or get_lang(), "values": {k: t(k, lang) for k in (keys or [])}}
