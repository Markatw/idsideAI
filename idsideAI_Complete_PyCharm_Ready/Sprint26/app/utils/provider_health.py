"""
Sprint 22.5 (protocol v2): Provider health check utilities.
"""

import time


def check_provider(name: str) -> dict:
    start = int(time.time() * 1000)
    # Simulate provider check (NOTE for real ping)
    ok = name.lower() != "bad"
    time.sleep(0.001)  # simulate small latency
    end = int(time.time() * 1000)
    return {"provider": name, "ok": ok, "latency_ms": end - start}
