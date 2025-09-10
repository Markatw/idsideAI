"""
Sprint 21.8 (protocol v2): Simple benchmark runner.
- run_bench(scenarios): measures latency and returns basic metrics per scenario.
Dependency-light; safe for server use.
"""

from typing import List, Dict, Any
import time


def _now_ms() -> int:
    return int(time.time() * 1000)


def run_bench(scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
    results = []
    for sc in scenarios or []:
        name = sc.get("name") or "scenario"
        # Simulated work: sleep for provided delay_ms (default 3ms)
        delay = int(sc.get("delay_ms", 3))
        start = _now_ms()
        time.sleep(max(0, delay) / 1000.0)
        end = _now_ms()
        latency = end - start
        results.append({"name": name, "latency_ms": latency, "ok": True})
    # Summary
    latencies = [r["latency_ms"] for r in results] or [0]
    summary = {
        "count": len(results),
        "p50_ms": int(sorted(latencies)[len(latencies) // 2]),
        "max_ms": int(max(latencies)),
        "min_ms": int(min(latencies)),
        "avg_ms": int(sum(latencies) / len(latencies)) if results else 0,
    }
    return {"results": results, "summary": summary}


from app.utils.perf import cap_events


def compare_providers(scenarios: list[dict], providers: list[str]) -> list[dict]:
    "Run scenarios across providers; simulate comparison."
    scenarios = cap_events(scenarios, max_items=50)
    results = []
    for prov in providers or []:
        prov_res = run_bench(scenarios)
        results.append(
            {
                "provider": prov,
                "results": prov_res["results"],
                "summary": prov_res["summary"],
            }
        )
    return results


def export_comparisons_csv(results: list[dict]) -> str:
    "Flatten comparison results into CSV string."
    from app.utils.perf import cap_events
    import io
    import csv

    rows = []
    for r in results or []:
        scenario = r.get("scenario", "")
        for entry in r.get("results") or []:
            rows.append(
                {
                    "scenario": scenario,
                    "provider": entry.get("provider", ""),
                    "latency_ms": entry.get("latency_ms", ""),
                    "ok": entry.get("ok", True),
                    "failure_type": entry.get("failure_type", ""),
                }
            )
    rows = cap_events(rows, max_items=10000)
    buf = io.StringIO()
    w = csv.DictWriter(
        buf, fieldnames=["scenario", "provider", "latency_ms", "ok", "failure_type"]
    )
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()
