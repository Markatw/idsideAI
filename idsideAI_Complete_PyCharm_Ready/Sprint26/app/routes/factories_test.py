"""
Sprint 26.2 — Factories test routes (protocol v2)
"""

from fastapi import APIRouter
from app.utils.factories import make_user, make_workspace, make_subscription

router = APIRouter(prefix="/api/factories", tags=["factories-test"])


@router.get("/user/{idx}")
def get_user(idx: int):
    return make_user(idx)


@router.get("/workspace/{idx}")
def get_workspace(idx: int):
    return make_workspace(idx)


@router.get("/subscription/{idx}")
def get_subscription(idx: int):
    return make_subscription(idx)
