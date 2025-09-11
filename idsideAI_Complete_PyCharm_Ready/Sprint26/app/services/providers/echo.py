"""
Sprint 21.4: Echo provider (protocol v2 default)
Provides a safe fallback that echoes input back.
"""

from typing import Any, Dict

from .base import BaseProvider
from .registry import register


class EchoProvider(BaseProvider):
    name = "echo"

    def health(self) -> Dict[str, Any]:
        return {"status": "ok", "provider": self.name}

    def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        return {"provider": self.name, "output": prompt, "meta": {"kwargs": kwargs}}


# register on import
register(EchoProvider.name, lambda cfg=None: EchoProvider(cfg or {}))
