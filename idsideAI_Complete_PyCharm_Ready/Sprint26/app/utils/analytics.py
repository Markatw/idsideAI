"""
Sprint 22.8 (protocol v2): Analytics JSONL logger.
- append_event(event): append dict to data/analytics_events.jsonl
- list_events(limit): return most recent events (capped)
"""
from typing import Dict, Any, List
import json, os
from app.utils.perf import cap_events

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "analytics_events.jsonl")

def _sanitize(event: Dict[str, Any]) -> Dict[str, Any]:
    # Keep only json-serializable primitives; coerce unknowns to str
    out = {}
    for k, v in (event or {}).items():
        try:
            json.dumps(v)
            out[str(k)] = v
        except Exception:
            out[str(k)] = str(v)
    return out

def append_event(event: Dict[str, Any]) -> Dict[str, Any]:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    e = _sanitize(event or {})
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return {"ok": True, "saved": e}

def list_events(limit: int = 1000) -> List[Dict[str, Any]]:
    if not os.path.exists(LOG_PATH):
        return []
    out: List[Dict[str, Any]] = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                out.append(json.loads(line.strip()))
            except Exception:
                continue
    # Return most recent first
    out = list(reversed(out))
    return cap_events(out, max_items=limit)
