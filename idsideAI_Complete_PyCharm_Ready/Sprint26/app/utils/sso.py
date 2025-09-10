"""
Sprint 25.3 — SSO utils (protocol v2)
Minimal helpers for SAML metadata & OIDC discovery.
"""
import json
from app.utils.perf import one_of as _one_of

def saml_metadata(entity_id: str, acs_url: str) -> str:
    eid = entity_id or "urn:idsideAI:sp"
    acs = acs_url or "https://example.com/api/sso/saml/acs"
    return f"<EntityDescriptor entityID=\"{eid}\"><SPSSODescriptor><AssertionConsumerService Location=\"{acs}\" Binding=\"urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST\"/></SPSSODescriptor></EntityDescriptor>"

def oidc_discovery(issuer: str, base_url: str) -> dict:
    iss = issuer or "https://example.com"
    base = base_url or iss
    return {
        "issuer": iss,
        "authorization_endpoint": f"{base}/api/sso/oidc/authorize",
        "token_endpoint": f"{base}/api/sso/oidc/token",
        "userinfo_endpoint": f"{base}/api/sso/oidc/userinfo",
        "jwks_uri": f"{base}/api/sso/oidc/jwks.json",
        "response_types_supported": ["code"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256"]
    }

def test_login(provider: str, email: str) -> dict:
    prov = _one_of(provider, ["saml","oidc"], "oidc")
    ok = bool(email and "@" in email)
    return {"ok": ok, "provider": prov, "email": email}
