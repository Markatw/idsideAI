"""
Sprint 21.4: Provider config schema (protocol v2)
A minimal schema validator (no external deps).
"""

from typing import Any, Dict

REQUIRED_KEYS = {
    "echo": [],
    "openai": ["api_key"],
    "anthropic": ["api_key"],
    "gemini": ["api_key"],
}


def validate(provider: str, config: Dict[str, Any]) -> Dict[str, Any]:
    need = REQUIRED_KEYS.get((provider or "echo").lower(), [])
    missing = [k for k in need if k not in (config or {})]
    return {"provider": provider, "missing": missing, "valid": len(missing) == 0}
