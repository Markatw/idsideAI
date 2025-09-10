"""
Sprint 26.2 — Test data factories (protocol v2)
"""
import uuid, random

def make_user(idx:int=1) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "email": f"user{idx}@example.com",
        "name": f"User {idx}",
        "active": True,
    }

def make_workspace(idx:int=1) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "name": f"Workspace {idx}",
        "plan": "free" if idx % 2 == 0 else "pro",
    }

def make_subscription(idx:int=1) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "status": "active" if idx % 2 == 0 else "trialing",
        "plan": "basic" if idx % 2 == 0 else "premium",
    }
