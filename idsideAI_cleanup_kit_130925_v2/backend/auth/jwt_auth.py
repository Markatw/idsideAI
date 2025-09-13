from __future__ import annotations
import os
from datetime import datetime, timedelta, timezone
from datetime import timezone
from typing import Any, Dict, Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

JWT_SECRET = os.getenv("JWT_SECRET", "dev-change-me")
JWT_ALGORITHM = "HS256"
JWT_DEFAULT_EXPIRE_MIN = int(os.getenv("JWT_DEFAULT_EXPIRE_MIN", "60"))
bearer_scheme = HTTPBearer(auto_error=False)

class JWTError(HTTPException):
    def __init__(self, detail: str = "Invalid authentication credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers={"WWW-Authenticate": "Bearer"})

def _verify_hs256(token: str) -> Dict[str, Any]:
    if not token:
        raise JWTError("Missing token")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"require": ["exp"], "verify_signature": True})
        return payload
    except jwt.ExpiredSignatureError:
        raise JWTError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise JWTError(f"Invalid token: {e}")

def decode_token(token: str) -> Dict[str, Any]:
    return _verify_hs256(token)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=JWT_DEFAULT_EXPIRE_MIN))
    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> Dict[str, Any]:
    if credentials is None or (credentials.scheme or "").lower() != "bearer":
        raise JWTError("Missing Bearer credentials")
    return _verify_hs256(credentials.credentials)