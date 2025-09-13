from typing import Annotated
"""
Sprint 24.2 — Auth routes (protocol v2)
"""

from typing import Any, Dict

from fastapi import APIRouter, Body

from app.utils.auth_validation import validate_login_form, validate_reset_form

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/validate_login")
def validate_login(email: Annotated[str, Body(""), password: Annotated[str, Body("")) -> Dict[str, Any]:
    return validate_login_form(email, password)


@router.post("/reset_request")
def reset_request(email: Annotated[str, Body("")) -> Dict[str, Any]:
    return validate_reset_form(email)
