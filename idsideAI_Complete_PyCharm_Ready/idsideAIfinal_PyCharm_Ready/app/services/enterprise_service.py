from typing import List, Optional

from app.models.enterprise import ApiCredential, DecisionModelShare
from app.utils.db import get_session
from sqlmodel import select


def set_api_key(user_id: Optional[int], provider: str, api_key: str) -> ApiCredential:
    with get_session() as session:
        # remove existing
        for row in session.exec(
            select(ApiCredential).where(
                ApiCredential.user_id == user_id, ApiCredential.provider == provider
            )
        ).all():
            session.delete(row)
        cred = ApiCredential(user_id=user_id, provider=provider, api_key=api_key)
        session.add(cred)
        session.commit()
        session.refresh(cred)
        return cred


def list_api_keys(user_id: Optional[int]) -> List[ApiCredential]:
    with get_session() as session:
        return session.exec(
            select(ApiCredential).where(ApiCredential.user_id == user_id)
        ).all()


def share_decision_model(dm_id: int, email: str, role: str = "viewer"):
    with get_session() as session:
        share = DecisionModelShare(
            decision_model_id=dm_id, shared_with_email=email, role=role
        )
        session.add(share)
        session.commit()
        session.refresh(share)
        return share


def list_shares(dm_id: int) -> List[DecisionModelShare]:
    with get_session() as session:
        return session.exec(
            select(DecisionModelShare).where(
                DecisionModelShare.decision_model_id == dm_id
            )
        ).all()
