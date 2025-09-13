from typing import Annotated
"""
Sprint 25.4 — PII crypto endpoints (protocol v2)
"""

from typing import Any, Dict

from fastapi import APIRouter, Body

from app.utils.pii_crypto import decrypt_pii, encrypt_pii

router = APIRouter(prefix="/api/crypto/pii", tags=["pii-crypto"])


@router.post("/encrypt")
def encrypt(value: Annotated[str, Body(""), key: Annotated[str, Body(...)) -> Dict[str, Any]:
    return {"token": encrypt_pii(value, key)}


@router.post("/decrypt")
def decrypt(token: Annotated[str, Body(""), key: Annotated[str, Body(...)) -> Dict[str, Any]:
    return {"value": decrypt_pii(token, key)}
