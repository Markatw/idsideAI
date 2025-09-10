"""
Sprint 24.4 — Graph tooltip injection (protocol v2)
"""
import re

def add_tooltips(svg: str, tooltips: dict) -> str:
    if not svg or not isinstance(svg, str):
        return svg
    out = svg
    for node_id, tip in (tooltips or {}).items():
        if not node_id or not tip:
            continue
        # Find element by id="..."
        pattern = rf'(<[^>]*id="{re.escape(node_id)}"[^>]*>)'
        repl = rf'\1<title>{tip}</title>'
        out, n = re.subn(pattern, repl, out, count=1)
    return out
