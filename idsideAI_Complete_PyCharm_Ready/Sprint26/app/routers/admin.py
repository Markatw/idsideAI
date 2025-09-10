
from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from .auth import _audit  # reuse existing audit helper

router = APIRouter(prefix="/admin")

SETTINGS_STORE: dict = {}
DEFAULT_SETTINGS = {"app_name": "idsideAI", "maintenance_mode": False, "rate_limit_signup_per_min": 5}


def _is_admin(req: Request) -> bool:
    u = req.session.get("user") if hasattr(req, "session") else None
    return bool(u and u.get("username") == "admin")

@router.get("/settings")
def get_settings(request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    _audit("admin_settings_get", "admin")
    return dict(SETTINGS_STORE)

@router.post("/settings")
def set_settings(request: Request, payload: dict):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    data = payload or {}
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="invalid settings payload")
    SETTINGS_STORE.update(data)
    _audit("admin_settings_set", "admin")
    _snapshot("admin")
    return {"ok": True, "count": len(data), "settings": dict(SETTINGS_STORE)}


@router.get("/settings/export")
def export_settings(request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    # Snapshot settings to canonical JSON bytes
    blob = json.dumps(dict(SETTINGS_STORE), ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
    import hashlib, base64
    digest = hashlib.sha256(blob).hexdigest()
    _audit("admin_settings_export", "admin")
    return {"filename": "settings.json", "bundle_b64": base64.b64encode(blob).decode("ascii"), "sha256": digest, "size": len(blob)}


@router.post("/settings/import")
def import_settings(request: Request, payload: dict):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    data = payload or {}
    blob_b64 = data.get("bundle_b64"); expect_hash = data.get("sha256"); mode = data.get("mode","replace")
    import base64, hashlib, json
    try:
        raw = base64.b64decode(blob_b64.encode("ascii")) if blob_b64 else None
    except Exception:
        raise HTTPException(status_code=400, detail="invalid base64")
    if not raw:
        raise HTTPException(status_code=400, detail="missing data")
    digest = hashlib.sha256(raw).hexdigest()
    if expect_hash and expect_hash != digest:
        raise HTTPException(status_code=400, detail="hash mismatch")
    try:
        newset = json.loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")
    if not isinstance(newset, dict):
        raise HTTPException(status_code=400, detail="settings must be dict")
    if mode == "replace":
        SETTINGS_STORE.clear(); SETTINGS_STORE.update(newset)
    else:
        SETTINGS_STORE.update(newset)
    _audit("admin_settings_import", "admin")
    _snapshot("admin")
    return {"ok": True, "count": len(newset), "sha256": digest, "mode": mode}


@router.post("/settings/reset")
def reset_settings(request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    SETTINGS_STORE.clear()
    SETTINGS_STORE.update(DEFAULT_SETTINGS)
    _audit("admin_settings_reset", "admin")
    _snapshot("admin")
    return {"ok": True, "settings": dict(SETTINGS_STORE)}


SETTINGS_HISTORY = []  # list of snapshots
HISTORY_MAX = 20

def _snapshot(user: str):
    SETTINGS_HISTORY.append({"ts": datetime.utcnow().isoformat(), "user": user, "settings": dict(SETTINGS_STORE)})
    if len(SETTINGS_HISTORY) > HISTORY_MAX:
        del SETTINGS_HISTORY[0]


@router.get("/settings/history")
def get_settings_history(request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    _audit("admin_settings_history_get", "admin")
    return {"count": len(SETTINGS_HISTORY), "history": list(SETTINGS_HISTORY)}

@router.post("/settings/rollback")
def rollback_settings(request: Request, payload: dict):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    idx = int((payload or {}).get("index", -1))
    if idx < 0 or idx >= len(SETTINGS_HISTORY):
        raise HTTPException(status_code=400, detail="invalid index")
    snap = SETTINGS_HISTORY[idx]
    SETTINGS_STORE.clear(); SETTINGS_STORE.update(dict(snap.get("settings", {})))
    _audit("admin_settings_rollback", "admin")
    _snapshot("admin")
    return {"ok": True, "restored_index": idx, "settings": dict(SETTINGS_STORE)}


@router.get("/settings/compliance-export")
def compliance_export(request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    meta = {"ts": datetime.utcnow().isoformat(), "user": "admin"}
    pack = {
        "settings": dict(SETTINGS_STORE),
        "history": list(SETTINGS_HISTORY),
        "meta": meta,
    }
    raw_settings = json.dumps(pack["settings"], ensure_ascii=False, indent=2).encode()
    raw_history = json.dumps(pack["history"], ensure_ascii=False, indent=2).encode()
    raw_meta = json.dumps(pack["meta"], ensure_ascii=False, indent=2).encode()
    import io, zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("settings.json", raw_settings)
        zf.writestr("history.json", raw_history)
        zf.writestr("meta.json", raw_meta)
    digest = hashlib.sha256(buf.getvalue()).hexdigest()
    zfinal = io.BytesIO()
    with zipfile.ZipFile(zfinal, "w", zipfile.ZIP_DEFLATED) as zf2:
        zf2.writestr("compliance.zip", buf.getvalue())
        zf2.writestr("SHA256.txt", digest)
    _audit("admin_settings_compliance_export", "admin")
    return {"filename": "settings_compliance.zip", "bundle_b64": base64.b64encode(zfinal.getvalue()).decode(), "sha256": digest, "history_count": len(SETTINGS_HISTORY)}
