"""
Sprint 21.4: Provider base interface (protocol v2)
Defines a minimal, dependency-free contract for provider adapters.
"""
from typing import Any, Dict

class ProviderError(Exception):
    def __init__(self, message: str, code: str = "provider_error", *, context: Dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.context = context or {}

    def __repr__(self) -> str:
        return f"<ProviderError code={self.code!r} message={self.args[0]!r} context={self.context!r}>"

    def __str__(self) -> str:
        return f"{self.code}: {self.args[0]}"

class BaseProvider:
    name: str = "base"

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}

    def health(self) -> Dict[str, Any]:
        return {"status": "unknown", "provider": self.name}

    def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        raise ProviderError("Not implemented", code="not_implemented", context={"method": "complete"})
