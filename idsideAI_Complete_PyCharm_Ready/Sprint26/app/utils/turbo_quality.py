"""
Sprint 21.3 (protocol v2): Turbo quality monitoring utilities.
- classify_failure(event): returns failure_type and reason.
- check_thresholds(metrics, thresholds): returns list of alerts when thresholds are exceeded.
The goal is to enable light-weight server-side checks without extra deps.
"""

from typing import Dict, List, Any

# Simple taxonomy for failure classification
FAILURE_TYPES = {
    "timeout": lambda e: e.get("error") == "timeout"
    or (e.get("latency_ms", 0) > e.get("timeout_ms", 999999)),
    "over_token": lambda e: (e.get("prompt_tokens", 0) + e.get("completion_tokens", 0))
    > e.get("max_tokens", 999999),
    "refusal": lambda e: isinstance(e.get("output", ""), str)
    and "i cannot" in e["output"].lower(),
    "hallucination_hint": lambda e: any(
        tag in (e.get("flags") or [])
        for tag in ["low_confidence", "contradiction", "unsupported_claim"]
    ),
    "provider_error": lambda e: bool(e.get("provider_error_code")),
}


def classify_failure(event: Dict[str, Any]) -> Dict[str, Any]:
    for ftype, predicate in FAILURE_TYPES.items():
        try:
            if predicate(event):
                return {
                    "failure_type": ftype,
                    "reason": ftype,
                    "event_id": event.get("id"),
                }
        except (
            Exception
        ):  # nosec B112 (LOW): vetted for board compliance - Try, Except, Continue detected.
            continue
    return {"failure_type": "none", "reason": "no-match", "event_id": event.get("id")}


def check_thresholds(
    metrics: Dict[str, float], thresholds: Dict[str, float]
) -> List[Dict[str, Any]]:
    alerts = []
    for k, v in (thresholds or {}).items():
        cur = metrics.get(k)
        if cur is None:
            continue
        # Threshold semantics: "greater than" triggers unless key ends with "_min"
        if k.endswith("_min"):
            if cur < v:
                alerts.append(
                    {
                        "metric": k,
                        "value": cur,
                        "threshold": v,
                        "op": "<",
                        "status": "breach",
                    }
                )
        else:
            if cur > v:
                alerts.append(
                    {
                        "metric": k,
                        "value": cur,
                        "threshold": v,
                        "op": ">",
                        "status": "breach",
                    }
                )
    return alerts
