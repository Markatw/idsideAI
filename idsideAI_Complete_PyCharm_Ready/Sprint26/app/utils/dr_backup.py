"""
Sprint 25.6 — DR backup/restore helpers (protocol v2)
"""

import zipfile
import time
from pathlib import Path


def backup_sqlite(db_path: str, out_dir: str) -> dict:
    p = Path(db_path)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = out / f"{p.stem or 'db'}_{ts}.bak.zip"
    with zipfile.ZipFile(bak, "w", compression=zipfile.ZIP_DEFLATED) as z:
        if p.exists():
            z.write(p, arcname=p.name)
        else:
            tmp = out / f"NOTE_{ts}.txt"
            tmp.write_text("no-source-db; NOTE", encoding="utf-8")
            z.write(tmp, arcname=tmp.name)
            tmp.unlink(missing_ok=True)
    return {"ok": True, "backup": str(bak), "source_exists": p.exists()}


def restore_sqlite(bak_zip: str, dest_dir: str) -> dict:
    bz = Path(bak_zip)
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    if not bz.exists():
        return {"ok": False, "error": "backup_not_found"}
    with zipfile.ZipFile(bz, "r") as z:
        z.extractall(dest)
    return {"ok": True, "restored_to": str(dest)}
