"""
Sprint 26.7 — Synthetic uptime probe (protocol v2)
"""
import time, requests

def check_url(url: str, timeout: int = 5) -> dict:
    t0 = time.time()
    try:
        r = requests.get(url, timeout=timeout)
        dt = int((time.time()-t0)*1000)
        return {"ok": r.status_code==200, "status": r.status_code, "dt_ms": dt}
    except Exception as e:
        dt = int((time.time()-t0)*1000)
        return {"ok": False, "status": 0, "error": str(e), "dt_ms": dt}

def uptime(urls: list[str]) -> dict:
    results = [check_url(u) for u in urls]
    ok = all(r["ok"] for r in results)
    return {"ok": ok, "results": results}
