from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TenantContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant = request.headers.get("X-Tenant", "demo-tenant")
        workspace = request.headers.get("X-Workspace", "demo-workspace")
        # attach to state
        request.state.tenant_id = tenant
        request.state.workspace_id = workspace
        response = await call_next(request)
        response.headers["X-Tenant"] = tenant
        response.headers["X-Workspace"] = workspace
        return response
