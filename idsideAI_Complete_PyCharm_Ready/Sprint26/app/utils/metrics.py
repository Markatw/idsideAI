"""
Sprint 25.7 — Metrics collector (protocol v2)
Very light in-process counters + histograms to expose Prometheus text format.
"""

COUNTERS = {
    "app_requests_total": 0,
    "app_health_checks_total": 0,
}
HISTOGRAMS = {
    "app_request_latency_seconds": [],  # store last N latencies (seconds)
}


def inc_counter(name: str, value: int = 1):
    COUNTERS[name] = COUNTERS.get(name, 0) + int(value or 0)


def observe_latency(name: str, seconds: float):
    arr = HISTOGRAMS.setdefault(name, [])
    arr.append(float(seconds))
    # Cap memory
    if len(arr) > 512:
        del arr[: len(arr) - 512]


def render_prometheus() -> str:
    lines = []
    for k, v in COUNTERS.items():
        lines.append(f"# TYPE {k} counter")
        lines.append(f"{k} {int(v)}")
    for k, arr in HISTOGRAMS.items():
        # simplistic summary: count and sum
        lines.append(f"# TYPE {k} histogram")
        count = len(arr)
        s = sum(arr) if arr else 0.0
        lines.append(f"{k}_count {count}")
        lines.append(f"{k}_sum {s:.6f}")
    return "\n".join(lines) + "\n"
