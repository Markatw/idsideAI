"""
Sprint 22.3 (protocol v2): Security middleware adding standard HTTP security headers.
Use by including: app.add_middleware(SecurityHeadersMiddleware)
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from typing import Callable

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request, call_next: Callable):
        response = await call_next(request)
        # Core headers
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        # Minimal, safe CSP for API-only surface
        response.headers.setdefault("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'; base-uri 'none'")
        return response


# R2: extra headers + simple tunables
DEFAULT_HSTS = "max-age=63072000; includeSubDomains; preload"
DEFAULT_COOP = "same-origin"
DEFAULT_COEP = "require-corp"
DEFAULT_CORP = "same-site"

class SecurityHeadersMiddlewareR2(SecurityHeadersMiddleware):
    def __init__(self, app: ASGIApp, *, enable_hsts: bool = True):
        super().__init__(app)
        self.enable_hsts = enable_hsts

    async def dispatch(self, request, call_next):
        response = await super().dispatch(request, call_next)
        # Existing minimal policy from R1 likely applied by parent.
        # R2 additions:
        response.headers.setdefault("Cross-Origin-Opener-Policy", DEFAULT_COOP)
        response.headers.setdefault("Cross-Origin-Embedder-Policy", DEFAULT_COEP)
        response.headers.setdefault("Cross-Origin-Resource-Policy", DEFAULT_CORP)
        if self.enable_hsts and request.url.scheme == "https":
            response.headers.setdefault("Strict-Transport-Security", DEFAULT_HSTS)
        return response
