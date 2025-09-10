"""
Sprint 22.5 — Provider health API (protocol v2)
- GET /api/providers/{name}/health -> single check
- GET /api/providers/health -> all providers
"""
from fastapi import APIRouter
from app.utils.provider_health import check_provider

router = APIRouter(prefix="/api/providers", tags=["providers"])

@router.get("/{name}/health")
def provider_health(name: str):
    return check_provider(name)

@router.get("/health")
def providers_health():
    providers = ["echo","bad","test"]
    return [check_provider(p) for p in providers]
