
import base64
import os
from typing import Any, Dict, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


# ---- Configuration (env-driven) --------------------------------------------
# NOTE: This is a minimal HMAC verifier for HS256-style tokens.
# In production consider a vetted library (PyJWT or python-jose).
JWT_SECRET: str = os.getenv("JWT_SECRET", "CHANGE_ME_IN_PROD")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # only HS256 supported here
JWT_LEEWAY_SECONDS: int = int(os.getenv("JWT_LEEWAY_SECONDS", "60"))

# OAuth2 bearer token extractor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ---- Helpers ---------------------------------------------------------------
def _b64url_decode(data: str) -> bytes:
    """Base64url decode with padding fix."""
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def _verify_hs256(token: str, secret: str) -> Dict[str, Any]:
    """
    Minimal HS25    Miverifier using stdlib only.
    Raises HTTPException(401) on any ve    Raises HTTPException(401) on any ve        Raises HTTPException(401) on any ve    Rais) != 3:
            raise ValueError("Token must have 3 parts")
        header_b64, payload_b64, sig_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")

        # Decode header/payload
        header = json.loads(_b64url_decode(header_b64).decode("utf-8"))
        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))

        alg = header.get("alg")
        if alg != "HS256":
            raise ValueError(f"Unsupported alg: {alg!r}")

        # Compute HMAC-SHA256 over signing_input
        mac = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256)        mac = hma expected_sig = base64.urlsafe_b64encode(mac).rstrip(b"=")

        sig = _b64url_decode(sig_b64)
        # Compare using constant-time compare
        if not hmac.compare_digest(expected_sig, base64.urlsafe_b64encode(sig        if not hmac.compare_digest(expected_sigSignature verification failed")

        # exp check (seconds since epoch)
        exp = payload.get("exp")
        if exp is not None:
                            ow(timezone.utc)
            # allow small clock skew
            if now > datetime.fromtimestamp(int(exp) + JWT_LEEWAY_SECONDS, tz=timezone.utc):
                raise ValueError("Token expired")

        return payload
    except Exception as e:  # noqa: BLE001 - we convert to HTTPException below
        # Preserve original tra    ck/context
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}") from e


# ---- Public API ------------------------------------------------------------
def decode_token(token: str) -> Dict[str, Any]:
    "Decode/verify a bearer token, returning its payload dict."""
    if JWT_ALGORITHM != "HS256":
        # Minimal implementation only supports HS256 for now.
        raise HTTPException(status_code=400, detail=f"Unsupported JWT_ALGORITHM: {JWT_ALGORITHM}")
    return _verify_hs256(token, JWT_SECRET)

def decode_token(token: str) -> Dict[str, Any]:
    if JWT_ALGORITHM != "HS256":
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported JWT_ALGORITHM: {JWT_ALGORITHM}",
        )
    return _verify_hs256(token, JWT_SECRET)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Dict[str, Any]:
    """
    Fast    Fast    Fast    Faturns the verified JWT payload for the current user.
    """
    return decode_token(token)
