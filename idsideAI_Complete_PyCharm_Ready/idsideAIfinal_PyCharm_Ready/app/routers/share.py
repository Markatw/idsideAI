from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.enterprise_service import share_decision_model, list_shares

router = APIRouter(prefix="/share", tags=["share"])


class ShareIn(BaseModel):
    dm_id: int
    email: str
    role: str = "viewer"  # viewer|editor|owner


@router.post("")
async def share(body: ShareIn):
    s = share_decision_model(body.dm_id, body.email, body.role)
    return {
        "id": s.id,
        "dm_id": s.decision_model_id,
        "email": s.shared_with_email,
        "role": s.role,
    }


@router.get("/{dm_id}")
async def shares(dm_id: int) -> List[dict]:
    out = []
    for s in list_shares(dm_id):
        out.append({"id": s.id, "email": s.shared_with_email, "role": s.role})
    return out
