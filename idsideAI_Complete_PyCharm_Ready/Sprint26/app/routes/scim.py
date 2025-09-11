"""
Sprint 25.2 — SCIM routes (protocol v2)
"""

from typing import Any, Dict

from fastapi import APIRouter, Body, Path, status
from fastapi.responses import JSONResponse

from app.utils.scim import list_response, user_skeleton

router = APIRouter(prefix="/scim/v2", tags=["scim"])


@router.get("/ServiceProviderConfig")
def sp_config():
    return {
        "patch": {"supported": True},
        "filter": {"supported": True},
        "bulk": {"supported": False},
        "changePassword": {"supported": False},
    }


@router.get("/Users")
def list_users() -> Dict[str, Any]:
    return list_response([])


@router.post("/Users", status_code=201)
def create_user(
    userName: str = Body(...),
    givenName: str = Body(""),
    familyName: str = Body(""),
    email: str = Body(""),
):
    return user_skeleton(userName, givenName, familyName, True, email)


@router.patch("/Users/{user_id}")
def patch_user(user_id: str = Path(...), active: bool = Body(True)):
    u = user_skeleton(userName=user_id, active=active)
    u["id"] = user_id
    return u


@router.delete("/Users/{user_id}")
def delete_user(user_id: str = Path(...)):
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
