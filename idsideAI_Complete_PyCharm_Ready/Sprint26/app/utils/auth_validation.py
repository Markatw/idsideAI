"""
Sprint 24.2 — Auth form validation helpers (protocol v2)
- a11y-friendly messages with field references and concise wording.
"""

import re

EMAIL_RX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _msg(field: str, text: str) -> dict:
    return {"field": field, "message": text, "aria_live": "polite"}


def validate_login_form(email: str, password: str) -> dict:
    errors = []
    if not email:
        errors.append(_msg("email", "Enter your email address."))
    elif not EMAIL_RX.match(str(email)):
        errors.append(_msg("email", "Enter an email in the format name@example.com."))
    if not password:
        errors.append(_msg("password", "Enter your password."))
    elif len(str(password)) < 8:
        errors.append(_msg("password", "Use at least 8 characters."))
    return {"ok": len(errors) == 0, "errors": errors}


def validate_reset_form(email: str) -> dict:
    if not email:
        return {"ok": False, "errors": [_msg("email", "Enter your email address.")]}
    if not EMAIL_RX.match(str(email)):
        return {
            "ok": False,
            "errors": [_msg("email", "Enter an email in the format name@example.com.")],
        }
    return {"ok": True, "errors": []}
