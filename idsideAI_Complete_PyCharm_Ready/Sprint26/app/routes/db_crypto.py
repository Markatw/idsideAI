from typing import Annotated
"""
Sprint 25.5 — DB crypto routes (protocol v2)
"""

import os
from typing import Any, Dict

from fastapi import APIRouter, Body

from app.utils.db_crypto import get_db_key

router = APIRouter(prefix="/api/db/enc", tags=["db-crypto"])


@router.get("/status")
def status() -> Dict[str, Any]:
    key = get_db_key()
    return {"enabled": bool(key), "key_loaded": bool(key)}


@router.post("/setkey")
def setkey(key: Annotated[str, Body(...)) -> Dict[str, Any]:
    os.environ["DB_ENC_KEY"] = key
    return {"ok": True, "enabled": True}
