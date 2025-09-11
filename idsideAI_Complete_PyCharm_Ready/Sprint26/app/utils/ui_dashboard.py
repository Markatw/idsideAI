"""
Sprint 24.3 — Dashboard UI helpers (protocol v2)
- responsive_cols(width) → 1/2/3/4 columns
- layout(tiles, width)  → grid positions
- validate_tiles(tiles) → basic a11y presence checks (title/ariaLabel)
"""

from app.utils.perf import cap_events, clamp_int


def responsive_cols(width: int) -> int:
    w = clamp_int(int(width or 0), 0, 10000)
    if w < 480:
        return 1
    if w < 768:
        return 2
    if w < 1200:
        return 3
    return 4


def layout(tiles: list[dict], width: int) -> list[dict]:
    tiles = cap_events(tiles or [], max_items=50)
    cols = responsive_cols(width)
    out = []
    r = c = 0
    for t in tiles:
        out.append(
            {
                "id": t.get("id"),
                "row": r,
                "col": c,
                "w": 1,
                "h": 1,
                "title": t.get("title"),
            }
        )
        c += 1
        if c >= cols:
            c = 0
            r += 1
    return out


def validate_tiles(tiles: list[dict]) -> dict:
    tiles = cap_events(tiles or [], max_items=50)
    errs = []
    for i, t in enumerate(tiles):
        if not t.get("title"):
            errs.append(
                {"index": i, "field": "title", "message": "Provide a tile title."}
            )
        if not t.get("ariaLabel"):
            errs.append(
                {"index": i, "field": "ariaLabel", "message": "Provide an aria-label."}
            )
    return {"ok": len(errs) == 0, "errors": errs}
