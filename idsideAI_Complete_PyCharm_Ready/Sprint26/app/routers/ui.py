from pathlib import Path

from fastapi import APIRouter, Response

router = APIRouter(prefix="/ui", tags=["ui"])


@router.get("")
def ui_root():
    p = Path(__file__).resolve().parents[1] / "static" / "index.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/onboarding")
def ui_onboarding():
    p = Path(__file__).resolve().parents[1] / "static" / "onboarding.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/workspaces")
def ui_workspaces():
    p = Path(__file__).resolve().parents[1] / "static" / "workspaces.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/dashboard")
def ui_dashboard():
    p = Path(__file__).resolve().parents[1] / "static" / "dashboard.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/viewer")
def ui_viewer():
    p = Path(__file__).resolve().parents[1] / "static" / "viewer.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/editor")
def ui_editor():
    p = Path(__file__).resolve().parents[1] / "static" / "editor.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/execute")
def ui_execute():
    p = Path(__file__).resolve().parents[1] / "static" / "execute.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/inspect")
def ui_inspect():
    p = Path(__file__).resolve().parents[1] / "static" / "inspect.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/search")
def ui_search():
    p = Path(__file__).resolve().parents[1] / "static" / "search.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/io")
def ui_io():
    p = Path(__file__).resolve().parents[1] / "static" / "io.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/admin")
def ui_admin():
    p = Path(__file__).resolve().parents[1] / "static" / "admin.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")


@router.get("/login")
def ui_login():
    p = Path(__file__).resolve().parents[1] / "static" / "login.html"
    return Response(content=p.read_text(encoding="utf-8"), media_type="text/html")
