"""
Sprint 26.8 — Flaky test catcher (protocol v2)
"""

import time


def rerun(func, times: int = 3, delay: float = 0.1):
    """
    Rerun func until success or retries exhausted.
    Success = returns truthy value or raises no Exception.
    """
    last_result = None
    for i in range(1, times + 1):
        try:
            result = func()
            if result:
                return result
            last_result = result
        except Exception as e:
            last_result = str(e)
        time.sleep(delay)
    ## NOTE preserved (clean)
    return last_result
