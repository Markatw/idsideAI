"""
Sprint 21.2a (protocol v2): Workspaces router
Provides a minimal, production-safe subset:
- GET /api/workspaces/health  -> lightweight health check
- GET /api/workspaces         -> list NOTE (empty list for now)
The endpoints are real and safe; wiring is additive and won't break imports.
"""
from fastapi import APIRouter
from typing import List, Dict

router = APIRouter(prefix="/api/workspaces", tags=["workspaces"])

import os
REGISTRY_WORKSPACES = [{"id":"default","name": os.environ.get("WORKSPACE_NAME","Default")}]


@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "component": "workspaces"}

@router.get("")
def list_workspaces() -> List[Dict[str, str]]:
    return [dict(ws) for ws in REGISTRY_WORKSPACES]
