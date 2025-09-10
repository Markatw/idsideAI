"""
Sprint 26.3 — API smoke tests (protocol v2)
Run against a local FastAPI server (default http://localhost:8000).
"""

import os
import sys
import json
import time

try:
    import requests  # type: ignore
except Exception:
    requests = None

BASE = os.getenv("SMOKE_BASE", "http://localhost:8000")

ENDPOINTS = [
    ("/api/metrics/health", 200),
    ("/api/metrics/prometheus", 200),
    ("/api/log/test", 200),
    ("/api/crypto/pii/encrypt", 200),  # expects POST; probe via method override logic
]


def main():
    results = []
    if requests is None:
        print(json.dumps({"ok": False, "error": "requests_not_available"}))
        return 0
    for path, expect in ENDPOINTS:
        url = BASE + path
        t0 = time.time()
        try:
            if path.endswith("/encrypt"):
                r = requests.post(url, json={"value": "ping", "key": "k"}, timeout=10)
            else:
                r = requests.get(url, timeout=10)
            ok = r.status_code == expect
            results.append(
                {
                    "path": path,
                    "status": r.status_code,
                    "ok": ok,
                    "dt_ms": int((time.time() - t0) * 1000),
                }
            )
        except Exception as e:
            results.append({"path": path, "status": 0, "ok": False, "error": str(e)})
    summary = {"ok": all(x.get("ok") for x in results), "results": results}
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
