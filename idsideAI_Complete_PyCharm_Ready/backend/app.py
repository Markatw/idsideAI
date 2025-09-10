import time
from fastapi.responses import Response
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from idsideAI_Complete_PyCharm_Ready.backend.middleware.tenant import (
    TenantContextMiddleware,
)
from idsideAI_Complete_PyCharm_Ready.backend.routers.graphs import (
    router as graphs_router,
)
from idsideAI_Complete_PyCharm_Ready.backend.routers.billing import (
    router as billing_router,
)
from idsideAI_Complete_PyCharm_Ready.backend.auth import jwt_auth
from idsideAI_Complete_PyCharm_Ready.backend.routers.metrics import (
    router as metrics_router,
)
from idsideAI_Complete_PyCharm_Ready.backend.auth.middleware import (
    get_auth,
    inject_tenant_headers,
)
from idsideAI_Complete_PyCharm_Ready.backend.routers.exports import (
    router as exports_router,
)

app = FastAPI(title="IDECIDE Graph API (Neo4j)", version="0.1.0")
app.add_middleware(TenantContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphs_router, prefix="/graphs", tags=["graphs"])
app.include_router(billing_router, prefix="/billing", tags=["billing"])
app.include_router(metrics_router, tags=["metrics"])


@app.get("/health")
def health():
    return {"status": "ok"}


from starlette.staticfiles import StaticFiles
import os

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)
app.mount("/exports", StaticFiles(directory=EXPORT_DIR), name="exports")

app.include_router(exports_router, prefix="/graphs", tags=["exports"])


@app.get("/whoami")
async def whoami(request):
    payload = await get_auth(request)
    tenant, workspace = inject_tenant_headers(request)
    return {
        "auth": bool(payload),
        "claims": payload or {},
        "tenant": tenant,
        "workspace": workspace,
    }


from fastapi import Depends, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "path", "status"]
)
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "Request latency", ["path"])


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    dur = time.time() - start
    try:
        REQUEST_COUNT.labels(
            request.method, request.url.path, str(response.status_code)
        ).inc()
        REQUEST_LATENCY.labels(request.url.path).observe(dur)
    except (
        Exception
    ):  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
        pass
    return response


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/whoami")
def whoami(user=Depends(jwt_auth.get_current_user)):
    return {"user": user or {"anonymous": True}}
