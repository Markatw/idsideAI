import os
import time
from typing import Any, Dict, Optional

import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

JWKS_URL = os.getenv("JWKS_URL")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")
JWT_ISSUER = os.getenv("JWT_ISSUER")
JWT_ALGORITHMS = os.getenv("JWT_ALGORITHMS", "RS256").split(",")

_http_bearer = HTTPBearer(auto_error=False)
_jwks_cache: Dict[str, Any] = {}
_jwks_cache_ts: float = 0.0
_JWKS_TTL = 300.0  # 5 minutes


def _get_jwks() -> Dict[str, Any]:
    global _jwks_cache, _jwks_cache_ts
    if not JWKS_URL:
        raise HTTPException(status_code=500, detail="JWKS_URL not configured")
    now = time.time()
    if _jwks_cache and (now - _jwks_cache_ts) < _JWKS_TTL:
        return _jwks_cache
    resp = requests.get(JWKS_URL, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    _jwks_cache = data
    _jwks_cache_ts = now
    return data


def _find_key(kid: str) -> Optional[Dict[str, Any]]:
    jwks = _get_jwks()
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    return None


def verify_token(token: str) -> Dict[str, Any]:
    try:
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        key = _find_key(kid) if kid else None
        options = {"verify_aud": bool(JWT_AUDIENCE)}
        claims = jwt.decode(
            token,
            key,
            algorithms=JWT_ALGORITHMS,
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
            options=options,
        )
        return claims
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}"
        )


def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(_http_bearer),
) -> Optional[Dict[str, Any]]:
    if not auth:
        return None  # allow public routes; handlers can choose to require
    token = auth.credentials
    return verify_token(token)
