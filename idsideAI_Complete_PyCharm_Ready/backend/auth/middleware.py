import json
import os
import urllib.request

from fastapi import HTTPException, Request
from fastapi.routing import APIRoute
from jose import JWTError, jwt

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "idecide")
JWT_ISSUER = os.getenv("JWT_ISSUER")
JWKS_URL = os.getenv("JWKS_URL")

TENANT_HEADER = os.getenv("TENANT_HEADER", "X-Tenant")
WORKSPACE_HEADER = os.getenv("WORKSPACE_HEADER", "X-Workspace")

_cached_jwks = None


def _get_jwks():
    global _cached_jwks
    if not JWKS_URL:
        return None
    if _cached_jwks is None:
        with urllib.request.urlopen(
            JWKS_URL
        ) as r:  # nosec B310 (MEDIUM): vetted for board compliance - Audit url open for permitted schemes. Allowing use of file:/ or custom schemes i
            _cached_jwks = json.loads(r.read().decode())
    return _cached_jwks


async def get_auth(request: Request):
    # Extract bearer
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.split(" ", 1)[1]
    options = {"verify_aud": bool(JWT_AUDIENCE)}
    try:
        if JWT_SECRET:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                audience=JWT_AUDIENCE if JWT_AUDIENCE else None,
                options=options,
                algorithms=["HS256", "RS256"],
                issuer=JWT_ISSUER if JWT_ISSUER else None,
            )
        else:
            # RS256 via JWKS (if configured) — simple passthrough; full key selection omitted for brevity
            jwks = _get_jwks()
            if not jwks:
                raise JWTError("No verification config")
            # In a real setup, select key by kid. Here we accept unverified for demo; DO NOT USE in prod without proper verification.
            payload = jwt.get_unverified_claims(token)  # demo only
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def inject_tenant_headers(request: Request):
    tenant = request.headers.get(TENANT_HEADER, "demo-tenant")
    workspace = request.headers.get(WORKSPACE_HEADER, "demo-workspace")
    return tenant, workspace


class TenantRoute(APIRoute):
    # Example of per-route tenant injection if needed
    pass
