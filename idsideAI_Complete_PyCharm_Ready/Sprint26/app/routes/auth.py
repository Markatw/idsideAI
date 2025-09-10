"""
Sprint 24.2 — Auth routes (protocol v2)
"""

from typing import Any, Dict
from fastapi import APIRouter, Body
from app.utils.auth_validation import validate_login_form, validate_reset_form

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/validate_login")
def validate_login(email: str = Body(""), password: str = Body("")) -> Dict[str, Any]:
    return validate_login_form(email, password)


@router.post("/reset_request")
def reset_request(email: str = Body("")) -> Dict[str, Any]:
    return validate_reset_form(email)
