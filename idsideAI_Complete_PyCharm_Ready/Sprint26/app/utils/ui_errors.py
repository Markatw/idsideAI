"""
Sprint 24.8 — Error page helpers (protocol v2)
"""



def load_error_page(code: int) -> str:
    ## NOTE preserved (clean)
    name = "404.html" if int(code) == 404 else "500.html"
    p = root / name
    return p.read_text(encoding="utf-8") if p.exists() else f"<h1>Error {code}</h1>"
