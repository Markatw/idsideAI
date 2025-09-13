from datetime import timezone
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request

from .auth import _audit

router = APIRouter(prefix="/workspaces")
WORKSPACES: dict = {}  # ws_id -> {id,name,owner,created_at}
MEMBERS: dict = {}
INVITES: dict = {}
ROLES: dict = {}
ACTIVITY: dict = {}
CHAT: dict = {}
PRESENCE: dict = {}
DOCS: dict = {}


def _is_admin(req: Request) -> bool:
    u = getattr(req, "session", {}).get("user") if hasattr(req, "session") else None
    return bool(u and u.get("username") == "admin")


@router.post("")
def create_ws(request: Request, payload: dict):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    name = (payload or {}).get("name") or "workspace"
    ws_id = (payload or {}).get("id") or uuid.uuid4().hex[:12]
    WORKSPACES[ws_id] = {
        "id": ws_id,
        "name": name,
        "owner": "admin",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "settings": {"title": name, "description": "", "plan": "free"},
    }
    _audit("ws_create", "admin")
    _activity_add(ws_id, "ws_create", "admin")
    ROLES.setdefault(ws_id, {})["admin"] = "owner"
    return WORKSPACES[ws_id]


@router.get("")
def list_ws(request: Request):
    if not _is_admin(request):
        raise HTTPException(status_code=403, detail="forbidden")
    _audit("ws_list", "admin")
    return {"count": len(WORKSPACES), "items": list(WORKSPACES.values())}


@router.delete("/{ws_id}")
def delete_ws(ws_id: str, request: Request):
    user = _user(request) or "admin"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    _require(ws_id, user, {"owner"})
    ok = bool(WORKSPACES.pop(ws_id, None))
    _audit("ws_delete", user)
    _activity_add(ws_id, "ws_delete", user)
    ROLES.pop(ws_id, None)
    MEMBERS.pop(ws_id, None)
    INVITES.pop(ws_id, None)
    if not ok:
        raise HTTPException(status_code=404, detail="not found")
    return {"ok": True, "id": ws_id}


def _user(req: Request):
    u = getattr(req, "session", {}).get("user") if hasattr(req, "session") else None
    return (u or {}).get("username")


@router.post("/{ws_id}/invite")
def invite_member(ws_id: str, request: Request, payload: dict):
    user = _user(request) or "admin"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    _require(ws_id, user, {"owner", "admin"})
    username = (payload or {}).get("username")
    if not username:
        raise HTTPException(status_code=400, detail="missing username")
    INVITES.setdefault(ws_id, set()).add(username)
    _audit("ws_invite", "admin")
    _activity_add(ws_id, "ws_invite", "admin", {"username": username})
    return {"ok": True, "invites": sorted(list(INVITES.get(ws_id, set())))}


@router.post("/{ws_id}/join")
def join_workspace(ws_id: str, request: Request):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in INVITES.get(ws_id, set()):
        raise HTTPException(status_code=403, detail="not invited")
    INVITES[ws_id].discard(user)
    MEMBERS.setdefault(ws_id, set()).add(user)
    _audit("ws_join", user)
    _activity_add(ws_id, "ws_join", user)
    return {"ok": True, "member": user, "members": sorted(list(MEMBERS[ws_id]))}


@router.post("/{ws_id}/leave")
def leave_workspace(ws_id: str, request: Request):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in MEMBERS.get(ws_id, set()):
        raise HTTPException(status_code=404, detail="not a member")
    MEMBERS[ws_id].discard(user)
    _audit("ws_leave", user)
    _activity_add(ws_id, "ws_leave", user)
    return {"ok": True, "member": user}


@router.get("/{ws_id}/members")
def list_members(ws_id: str, request: Request):
    user = _user(request) or "admin"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    _require(ws_id, user, {"owner", "admin"})
    return {
        "members": sorted(list(MEMBERS.get(ws_id, set()))),
        "invites": sorted(list(INVITES.get(ws_id, set()))),
    }


def _role(ws_id: str, user: str) -> str:
    return (ROLES.get(ws_id, {}) or {}).get(user, "member")


def _require(ws_id: str, user: str, allowed: set):
    if _role(ws_id, user) not in allowed:
        raise HTTPException(status_code=403, detail="insufficient role")


@router.post("/{ws_id}/roles")
def set_role(ws_id: str, request: Request, payload: dict):
    actor = _user(request) or "admin"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    tgt = (payload or {}).get("username")
    role = (payload or {}).get("role")
    if role not in {"owner", "admin", "member"}:
        raise HTTPException(status_code=400, detail="invalid role")
    if role == "owner":
        _require(ws_id, actor, {"owner"})
    else:
        _require(ws_id, actor, {"owner", "admin"})
    ROLES.setdefault(ws_id, {})[tgt] = role
    _audit("ws_role_set", actor)
    _activity_add(ws_id, "ws_role_set", actor, {"username": tgt, "role": role})
    return {"ok": True, "username": tgt, "role": role}


def _ctx_get(req: Request):
    sess = getattr(req, "session", None)
    return (sess or {}).get("ws_id") if isinstance(sess, dict) else None


def _ctx_set(req: Request, ws_id: str):
    if not hasattr(req, "session") or not isinstance(req.session, dict):
        req.session = {}
    req.session["ws_id"] = ws_id


def require_workspace_context(request: Request) -> str:
    ws_id = _ctx_get(request)
    if not ws_id or ws_id not in WORKSPACES:
        raise HTTPException(status_code=400, detail="workspace context not set")
    return ws_id


@router.post("/switch")
def switch_workspace(request: Request, payload: dict):
    user = _user(request) or "guest"
    ws_id = (payload or {}).get("ws_id")
    if not ws_id or ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in MEMBERS.get(ws_id, set()) and _role(ws_id, user) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not a member")
    _ctx_set(request, ws_id)
    _audit("ws_switch", user)
    _activity_add(ws_id, "ws_switch", user)
    _presence_touch(ws_id, user)
    return {"ok": True, "ws_id": ws_id, "role": _role(ws_id, user)}


@router.get("/context")
def get_context(request: Request):
    ws_id = _ctx_get(request)
    return {"ws_id": ws_id, "valid": bool(ws_id in WORKSPACES) if ws_id else False}


@router.get("/{ws_id}/settings")
def get_settings(ws_id: str, request: Request):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in MEMBERS.get(ws_id, set()) and _role(ws_id, user) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    return WORKSPACES[ws_id].get("settings", {})


@router.patch("/{ws_id}/settings")
def patch_settings(ws_id: str, request: Request, payload: dict):
    actor = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    _require(ws_id, actor, {"owner", "admin"})
    st = WORKSPACES[ws_id].setdefault(
        "settings", {"title": "", "description": "", "plan": "free"}
    )
    for k in ("title", "description", "plan"):
        if k in (payload or {}):
            st[k] = payload[k]
    _audit("ws_settings_update", actor)
    _activity_add(ws_id, "ws_settings_update", actor)
    return st


def _activity_add(ws_id: str, event: str, actor: str, extra: dict | None = None):
    ACTIVITY.setdefault(ws_id, []).append(
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "actor": actor,
            "extra": extra or {},
        }
    )


@router.get("/{ws_id}/activity")
def get_activity(ws_id: str, request: Request, limit: int = 50):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in MEMBERS.get(ws_id, set()) and _role(ws_id, user) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    items = ACTIVITY.get(ws_id, [])
    lim = max(0, min(int(limit), 200))
    return {"count": len(items), "items": items[-lim:]}


@router.get("/{ws_id}/export")
def export_audit(ws_id: str, request: Request):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    # members, admins, owners may export
    if user not in MEMBERS.get(ws_id, set()) and _role(ws_id, user) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    ws = WORKSPACES[ws_id]
    return {
        "workspace": {
            "id": ws_id,
            "name": ws.get("name"),
            "created_at": ws.get("created_at"),
        },
        "settings": ws.get("settings", {}),
        "roles": ROLES.get(ws_id, {}),
        "members": sorted(list(MEMBERS.get(ws_id, set()))),
        "invites": sorted(list(INVITES.get(ws_id, set()))),
        "activity": ACTIVITY.get(ws_id, []),
        "chat": CHAT.get(ws_id, []),
        "docs": list((DOCS.get(ws_id, {}) or {}).values()),
        "presence": PRESENCE.get(ws_id, {}),
    }


def _chat_add(ws_id: str, user: str, text: str):
    CHAT.setdefault(ws_id, []).append(
        {"ts": datetime.now(timezone.utc).isoformat(), "user": user, "text": text}
    )


@router.post("/{ws_id}/chat")
def post_chat(ws_id: str, request: Request, payload: dict):
    actor = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if actor not in MEMBERS.get(ws_id, set()) and _role(ws_id, actor) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    text = (payload or {}).get("text")
    if not text or not isinstance(text, str):
        raise HTTPException(status_code=400, detail="missing text")
    _chat_add(ws_id, actor, text)
    _presence_touch(ws_id, actor)
    _activity_add(ws_id, "chat_post", actor, {"chars": len(text)})
    return {"ok": True, "count": len(CHAT.get(ws_id, []))}


@router.get("/{ws_id}/chat")
def get_chat(ws_id: str, request: Request, limit: int = 50):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in MEMBERS.get(ws_id, set()) and _role(ws_id, user) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    msgs = CHAT.get(ws_id, [])
    lim = max(0, min(int(limit), 200))
    return {"count": len(msgs), "items": msgs[-lim:]}


def _presence_touch(ws_id: str, user: str):
    PRESENCE.setdefault(ws_id, {})[user] = datetime.now(timezone.utc).isoformat()


@router.get("/{ws_id}/presence")
def get_presence(ws_id: str, request: Request):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in MEMBERS.get(ws_id, set()) and _role(ws_id, user) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    pres = PRESENCE.get(ws_id, {})
    items = [{"user": u, "last_seen": ts} for u, ts in pres.items()]
    return {"count": len(items), "members": items}


def _doc_make(ws_id: str, doc_id: str, title: str, content: str, owner: str):
    DOCS.setdefault(ws_id, {})[doc_id] = {
        "id": doc_id,
        "title": title,
        "content": content,
        "owner": owner,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": None,
    }


@router.post("/{ws_id}/docs")
def create_doc(ws_id: str, request: Request, payload: dict):
    actor = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if actor not in MEMBERS.get(ws_id, set()) and _role(ws_id, actor) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    doc_id = (payload or {}).get("id")
    title = (payload or {}).get("title") or ""
    content = (payload or {}).get("content") or ""
    if not doc_id or not isinstance(doc_id, str):
        raise HTTPException(status_code=400, detail="missing id")
    if doc_id in (DOCS.get(ws_id, {}) or {}):
        raise HTTPException(status_code=409, detail="doc exists")
    _doc_make(ws_id, doc_id, title, content, actor)
    _activity_add(ws_id, "doc_create", actor, {"id": doc_id})
    return DOCS[ws_id][doc_id]


@router.get("/{ws_id}/docs/{doc_id}")
def read_doc(ws_id: str, doc_id: str, request: Request):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES or ws_id not in DOCS:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in MEMBERS.get(ws_id, set()) and _role(ws_id, user) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    doc = DOCS[ws_id].get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="doc not found")
    return doc


@router.patch("/{ws_id}/docs/{doc_id}")
def update_doc(ws_id: str, doc_id: str, request: Request, payload: dict):
    actor = _user(request) or "guest"
    if ws_id not in WORKSPACES or ws_id not in DOCS:
        raise HTTPException(status_code=404, detail="workspace not found")
    doc = DOCS[ws_id].get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="doc not found")
    # owner or admin may edit
    if actor != doc.get("owner") and _role(ws_id, actor) not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="not allowed")
    if "title" in (payload or {}):
        doc["title"] = payload["title"]
    if "content" in (payload or {}):
        doc["content"] = payload["content"]
    doc["updated_at"] = datetime.now(timezone.utc).isoformat()
    _activity_add(ws_id, "doc_update", actor, {"id": doc_id})
    return doc


@router.get("/{ws_id}/docs")
def list_docs(ws_id: str, request: Request, limit: int = 100):
    user = _user(request) or "guest"
    if ws_id not in WORKSPACES:
        raise HTTPException(status_code=404, detail="workspace not found")
    if user not in MEMBERS.get(ws_id, set()) and _role(ws_id, user) not in {
        "owner",
        "admin",
    }:
        raise HTTPException(status_code=403, detail="not allowed")
    bucket = DOCS.get(ws_id, {}) or {}
    items = list(bucket.values())
    lim = max(0, min(int(limit), 500))
    return {"count": len(items), "items": items[:lim]}


@router.delete("/{ws_id}/docs/{doc_id}")
def delete_doc(ws_id: str, doc_id: str, request: Request):
    actor = _user(request) or "guest"
    if ws_id not in WORKSPACES or ws_id not in DOCS:
        raise HTTPException(status_code=404, detail="workspace not found")
    doc = DOCS[ws_id].get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="doc not found")
    if actor != doc.get("owner") and _role(ws_id, actor) not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="not allowed")
    DOCS[ws_id].pop(doc_id, None)
    _activity_add(ws_id, "doc_delete", actor, {"id": doc_id})
    return {"ok": True}
