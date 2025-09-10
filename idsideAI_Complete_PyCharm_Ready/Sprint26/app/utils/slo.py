"""
Sprint 26.6 — Error budget tracker (protocol v2)
"""

_total = 0
_errors = 0
BUDGET = 0.01  # 1% allowed error rate


def record(success: bool):
    global _total, _errors
    _total += 1
    if not success:
        _errors += 1


def status() -> dict:
    if _total == 0:
        err_rate = 0.0
    else:
        err_rate = _errors / _total
    remaining = max(0.0, BUDGET - err_rate)
    return {
        "total": _total,
        "errors": _errors,
        "error_rate": round(err_rate * 100, 2),
        "budget": BUDGET * 100,
        "remaining_budget": round(remaining * 100, 2),
    }
