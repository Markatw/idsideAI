"""
Sprint 25.4 — PII crypto endpoints (protocol v2)
"""
from typing import Any, Dict
from fastapi import APIRouter, Body
from app.utils.pii_crypto import encrypt_pii, decrypt_pii

router = APIRouter(prefix="/api/crypto/pii", tags=["pii-crypto"])

@router.post("/encrypt")
def encrypt(value: str = Body(""), key: str = Body(...)) -> Dict[str, Any]:
    return {"token": encrypt_pii(value, key)}

@router.post("/decrypt")
def decrypt(token: str = Body(""), key: str = Body(...)) -> Dict[str, Any]:
    return {"value": decrypt_pii(token, key)}
