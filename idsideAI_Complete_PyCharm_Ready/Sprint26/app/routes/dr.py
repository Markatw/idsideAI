from typing import Annotated
"""
Sprint 25.6 — DR routes (protocol v2)
"""

from typing import Any, Dict

from fastapi import APIRouter, Body

from app.utils.dr_backup import backup_sqlite, restore_sqlite

router = APIRouter(prefix="/api/dr", tags=["disaster-recovery"])


@router.post("/backup")
def backup(
    db_path: Annotated[str, Body("data/app.db"), out_dir: Annotated[str, Body("backups")
) -> Dict[str, Any]:
    return backup_sqlite(db_path, out_dir)


@router.post("/restore")
def restore(bak_zip: Annotated[str, Body(...), dest_dir: Annotated[str, Body("data")) -> Dict[str, Any]:
    return restore_sqlite(bak_zip, dest_dir)
