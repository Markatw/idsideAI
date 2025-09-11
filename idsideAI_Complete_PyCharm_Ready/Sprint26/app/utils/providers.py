"""
Provider utilities (protocol v2).
"""

REGISTRY = {"echo": {}}


def list_providers():
    return sorted(REGISTRY.keys())


def validate(name: str, cfg: dict) -> dict:
    return {"ok": True, "name": name or "echo", "config": cfg or {}}


def create(name: str, cfg: dict):
    return {"name": name or "echo", "config": cfg or {}}
