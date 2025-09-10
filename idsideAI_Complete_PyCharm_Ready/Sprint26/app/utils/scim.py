"""
Sprint 25.2 — SCIM utils (protocol v2)
Minimal helpers for SCIM Users payloads.
"""
from uuid import uuid4

SCHEMAS_USER = ["urn:ietf:params:scim:schemas:core:2.0:User"]

def user_skeleton(userName: str, givenName: str = "", familyName: str = "", active: bool = True, email: str = "") -> dict:
    uid = str(uuid4())
    return {
        "schemas": SCHEMAS_USER,
        "id": uid, "userName": userName,
        "name": {"givenName": givenName, "familyName": familyName},
        "active": active,
        "emails": [{"value": email, "primary": True}] if email else []
    }

def list_response(resources: list[dict], start: int = 1) -> dict:
    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(resources),
        "startIndex": start,
        "itemsPerPage": len(resources),
        "Resources": resources
    }
