"""Telemetry CSV export utility (protocol v2)."""
import csv, io
from app.utils.perf import cap_events

def export_events_csv(events: list[dict]) -> str:
    events = cap_events(events)
    """Export telemetry events to CSV string (extended fields: provider, latency_ms, failure_type)."""
    if not events:
        return ""
    fields = set()
    for e in events:
        fields.update(e.keys())
    # Ensure core + extended fields ordering
    core = ["id", "timestamp", "provider", "latency_ms", "failure_type", "status"]
    cols = core + [f for f in sorted(fields) if f not in core]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols)
    w.writeheader()
    for e in events:
        row = {k: e.get(k, "") for k in cols}
        w.writerow(row)
    return buf.getvalue()

def summarize_events(events: list[dict]) -> dict:
    """Summarize telemetry events: count, avg latency, failure counts."""
    if not events:
        return {"count":0,"avg_latency":0,"failures":0}
    n = len(events)
    latencies = [int(e.get("latency_ms",0)) for e in events if "latency_ms" in e]
    avg_lat = sum(latencies)//len(latencies) if latencies else 0
    failures = sum(1 for e in events if e.get("failure_type"))
    return {"count":n,"avg_latency":avg_lat,"failures":failures}


def summarize_events(events: list[dict]) -> dict:
    """Enriched summary: totals, avg latency, failure rate, providers used."""
    events = cap_events(events or [], max_items=10000)
    total = len(events)
    latencies = [int(e.get("latency_ms", 0)) for e in events if "latency_ms" in e]
    avg_latency_ms = (sum(latencies) // len(latencies)) if latencies else 0
    failures = sum(1 for e in events if e.get("failure_type"))
    failure_rate = (failures / total) if total else 0.0
    providers = sorted({str(e.get("provider","")) for e in events if e.get("provider")})
    return {
        "total_events": total,
        "avg_latency_ms": int(avg_latency_ms),
        "failures": int(failures),
        "failure_rate": float(round(failure_rate, 4)),
        "providers_used": providers
    }
