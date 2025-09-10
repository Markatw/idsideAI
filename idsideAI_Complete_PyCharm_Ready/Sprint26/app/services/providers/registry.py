"""
Sprint 21.4: Provider registry (protocol v2)
Lightweight discovery and graceful fallback if provider missing.
"""
from typing import Dict, Any, Optional, Callable
from .base import BaseProvider, ProviderError

_REGISTRY: Dict[str, Callable[..., BaseProvider]] = {}

def register(name: str, factory: Callable[..., BaseProvider]):
    _REGISTRY[name.lower()] = factory

def create(name: str, config: Dict[str, Any] | None = None) -> BaseProvider:
    key = (name or "echo").lower()
    factory = _REGISTRY.get(key) or _REGISTRY.get("echo")
    if not factory:
        # absolute fallback
        from .echo import EchoProvider
        return EchoProvider(config or {})
    return factory(config or {})
