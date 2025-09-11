"""
Sprint 25.3 — SSO routes (protocol v2)
"""

from typing import Any, Dict

from fastapi import APIRouter, Body, Query
from fastapi.responses import HTMLResponse

from app.utils.sso import oidc_discovery, saml_metadata, test_login

router = APIRouter(prefix="/api/sso", tags=["sso"])


@router.get("/saml/metadata", response_class=HTMLResponse)
def saml_metadata_xml(entity_id: str = Query(""), acs_url: str = Query("")) -> str:
    return saml_metadata(entity_id, acs_url)


@router.get("/oidc/.well-known/openid-configuration")
def oidc_config(issuer: str = Query(""), base_url: str = Query("")) -> Dict[str, Any]:
    return oidc_discovery(issuer, base_url)


@router.post("/test")
def sso_test(provider: str = Body("oidc"), email: str = Body("")) -> Dict[str, Any]:
    return test_login(provider, email)
