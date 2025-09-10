"""
Sprint 25.8 — Log test route (protocol v2)
"""

from fastapi import APIRouter
from app.utils.logging import get_logger

router = APIRouter(prefix="/api/log", tags=["log-test"])
logger = get_logger("log-test")


@router.get("/test")
def log_test():
    logger.info("Structured log test OK")
    return {"ok": True}
