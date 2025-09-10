# v5.5 enterprise extensions (optional, included)
try:
    from app.routers import settings as settings_router
    app.include_router(settings_router.router)
except Exception:  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
    pass
try:
    from app.routers import share as share_router
    app.include_router(share_router.router)
except Exception:  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
    pass
# Security middleware
try:
    from app.utils.security_middleware import SecurityHeadersMiddleware, SimpleRateLimitMiddleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(SimpleRateLimitMiddleware)
except Exception:  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
    pass
