"""
Sprint 25.5 — DB encryption helper (protocol v2)
Simulated DB encryption at rest config (hook for SQLCipher or TDE).
"""
import os

def get_db_key() -> str:
    return os.getenv("DB_ENC_KEY","")

def wrap_sqlite_conn(path: str) -> dict:
    key = get_db_key()
    enabled = bool(key)
    return {"db_path": path, "enabled": enabled, "note": "Simulated encryption wrapper"}
