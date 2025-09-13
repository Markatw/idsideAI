from datetime import timezone
from datetime import datetime
from typing import Any, Dict, List


class Telemetry:
    _events: List[Dict[str, Any]] = []

    @classmethod
    def log(cls, provider: str, metrics: Dict[str, Any]):
        cls._events.append(
            {"ts": datetime.now(timezone.utc).isoformat(), "provider": provider, **metrics}
        )

    @classmethod
    def dump(cls) -> List[Dict[str, Any]]:
        return list(cls._events)
