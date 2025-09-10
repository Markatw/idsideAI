"""
Sprint 28.6 — Enterprise feature flag toggle (protocol v2)
Centralized feature flag reader with env-backed booleans.
"""
import os
from typing import Dict

DEFAULTS: Dict[str, bool] = {
    "REFERRAL_ENGINE_ENABLED": os.getenv("REFERRAL_ENGINE_ENABLED", "false").lower() == "true",
    "STRIPE_ENABLED": bool(os.getenv("STRIPE_SECRET_KEY")),
    "I18N_FINAL_ENABLED": os.getenv("I18N_FINAL_ENABLED", "false").lower() == "true",
    "PEN_TEST_SCAN_ENABLED": os.getenv("PEN_TEST_SCAN_ENABLED", "false").lower() == "true",
}

def get_flag(name: str) -> bool:
    return bool(DEFAULTS.get(name, False))

def all_flags() -> Dict[str, bool]:
    return dict(DEFAULTS)
