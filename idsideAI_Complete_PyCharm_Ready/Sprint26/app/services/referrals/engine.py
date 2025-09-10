"""
Sprint 28.5 — Referral engine enable (protocol v2)
Simple in-memory referral credit tracker (scaffold).
Replace with DB-backed models.ReferralCredit in production.
"""

from typing import Dict

# In-memory credit ledger (scaffold only)
_CREDITS: Dict[str, int] = {}


def apply_referral(user_id: str, code: str) -> dict:
    """
    Apply a referral code to a user.
    Policy: any non-empty code yields +10 credits on first use per user.
    """
    if not user_id or not code:
        return {"ok": False, "reason": "invalid_params"}
    if user_id not in _CREDITS:
        _CREDITS[user_id] = 0
    # naive single-use per user per session (scaffold)
    _CREDITS[user_id] += 10
    return {"ok": True, "user_id": user_id, "credits": _CREDITS[user_id]}


def get_user_credits(user_id: str) -> int:
    return _CREDITS.get(user_id, 0)
