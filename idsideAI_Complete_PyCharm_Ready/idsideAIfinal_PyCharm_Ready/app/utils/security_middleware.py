from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        resp: Response = await call_next(request)
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Referrer-Policy"] = "same-origin"
        return resp


class SimpleRateLimitMiddleware(BaseHTTPMiddleware):
    WINDOW = 10.0
    LIMIT = 50
    hits = {}

    async def dispatch(self, request, call_next):
        now = time.time()
        key = request.client.host if request.client else "anon"
        bucket = self.hits.get(key, [])
        bucket = [t for t in bucket if now - t < self.WINDOW]
        if len(bucket) >= self.LIMIT:
            return Response("Too Many Requests", status_code=429)
        bucket.append(now)
        self.hits[key] = bucket
        return await call_next(request)
