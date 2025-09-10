"""
Sprint 24.7 — Accessibility overlay widget utils (protocol v2)
- scan_page(html) → detect missing alt, aria-label, bad contrast.
"""

import re


def scan_page(html: str) -> dict:
    issues = []
    if not html:
        return {"ok": True, "issues": []}
    # img without alt
    for m in re.finditer(r"<img [^>]*>", html, re.I):
        if "alt=" not in m.group(0).lower():
            issues.append({"type": "img_alt", "snippet": m.group(0)})
    # elements without aria-label where required (buttons)
    for m in re.finditer(r"<button[^>]*>", html, re.I):
        if "aria-label" not in m.group(0).lower():
            issues.append({"type": "btn_aria", "snippet": m.group(0)})
    # naive contrast check: flag black text on black bg
    if re.search(r"color:\s*#000", html, re.I) and re.search(
        r"background(-color)?:\s*#000", html, re.I
    ):
        issues.append({"type": "contrast", "snippet": "#000 on #000"})
    return {"ok": len(issues) == 0, "issues": issues}
