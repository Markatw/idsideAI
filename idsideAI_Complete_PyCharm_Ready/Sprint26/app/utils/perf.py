"""
Sprint 22.4 (protocol v2): Lightweight performance helpers.
"""
from functools import lru_cache
from typing import Iterable, Callable
__all__ = ['one_of']

def one_of(*values, default=None):
    """Return first non-empty value among *values, else default.
    Empty means: None, '', [], {}, (), or whitespace-only strings.
    """
    sentinel = (None, '', [], {}, ())
    for v in values:
        if isinstance(v, str) and v.strip()=='' :
            continue
        if v not in sentinel:
            return v
    return default


def memoize_small(maxsize: int = 128):
    "Return a decorator that applies lru_cache with a small bounded size."
    def deco(fn: Callable):
        return lru_cache(maxsize=maxsize)(fn)
    return deco

def clamp_int(value: int, lo: int, hi: int) -> int:
    try:
        v = int(value)
    except Exception:
        return lo
    if v < lo: 
        return lo
    if v > hi:
        return hi
    return v

def cap_events(events: list, max_items: int = 10000) -> list:
    "Return at most max_items events (defensive cap for exports/summaries)."
    if not isinstance(events, list):
        return []
    if len(events) <= max_items:
        return events
    return events[:max_items]
