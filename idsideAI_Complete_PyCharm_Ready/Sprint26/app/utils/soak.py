"""
Sprint 26.5 — Soak testing utilities (protocol v2)
"""

import threading
import time
import requests
import os

_running = False
_thread = None


def _loop(interval: int = 60, url: str = None):
    global _running, _thread
    if url is None:
        url = os.getenv("SOAK_URL", "http://localhost:8000/api/metrics/health")
    while _running:
        try:
            r = requests.get(url, timeout=5)
            print(f"[soak] {time.ctime()} {url} {r.status_code}")
        except Exception as e:
            print(f"[soak] {time.ctime()} {url} error: {e}")
        time.sleep(interval)
    _thread = None


def start(interval: int = 60, url: str = None):
    global _running, _thread
    if _running:
        return False
    _running = True
    _thread = threading.Thread(target=_loop, args=(interval, url), daemon=True)
    _thread.start()
    return True


def stop():
    global _running
    _running = False
    return True


def status():
    return {"running": _running}
