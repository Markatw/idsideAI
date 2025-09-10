"""
Sprint 24.5 — Theme tokens + toggle (protocol v2)
- get_tokens(mode) -> CSS vars map
- toggle_mode(pref) -> 'light'/'dark' (guards)
"""
from app.utils.perf import one_of as _one_of

LIGHT = {
    "--bg":"#ffffff","--fg":"#0f172a","--muted":"#475569",
    "--card":"#f8fafc","--border":"#e2e8f0","--accent":"#2563eb"
}
DARK = {
    "--bg":"#0b1220","--fg":"#e5e7eb","--muted":"#94a3b8",
    "--card":"#111827","--border":"#1f2937","--accent":"#60a5fa"
}

def get_tokens(mode: str = "light") -> dict:
    m = _one_of(mode, ["light","dark"], "light")
    return {"mode": m, "vars": (LIGHT if m=="light" else DARK)}

def toggle_mode(pref: str) -> str:
    m = _one_of(pref, ["light","dark","auto"], "auto")
    if m == "auto":  # caller can resolve via prefers-color-scheme
        return "auto"
    return "dark" if m=="light" else "light"
