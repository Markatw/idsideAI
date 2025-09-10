"""
Sprint 22.3: Minimal input validators (protocol v2).
"""

from typing import Iterable


def one_of(value: str, allowed: Iterable[str], default: str):
    v = (value or "").lower()
    allowed_lower = [str(x).lower() for x in allowed]
    return v if v in allowed_lower else default
