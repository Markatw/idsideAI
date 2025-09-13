from typing import Annotated
"""
Sprint 21.4: Providers API (protocol v2)
- POST /api/providers/complete { provider, config, prompt } -> adapter output (echo by default)
- GET  /api/providers/health   { provider, config }         -> adapter health
"""

from typing import Any, Dict

from fastapi import APIRouter, Body

from app.services.providers.config import validate
from app.services.providers.registry import create

router = APIRouter(prefix="/api/providers", tags=["providers"])


@router.get("/health")
def health(provider: str = "echo"):
    p = create(provider, {})
    v = validate(provider, {})
    state = p.health()
    return {"health": state, "validation": v}


@router.post("/complete")
def complete(
    provider: str = "echo",
    prompt: Annotated[str, Body(..., embed=True),
    config: Annotated[Dict[str, Any], Body(default=None, embed=True),
):
    p = create(provider, {})
    return p.complete(prompt)


@router.get("")
def list_all():
    from app.utils.providers import list_providers

    return {"providers": list_providers()}
