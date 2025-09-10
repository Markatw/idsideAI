from idsideAI_Complete_PyCharm_Ready.backend.compat.optional_deps import (
    prometheus_client as _pc,
)

if _pc:
    from prometheus_client import (
        Counter,
        Histogram,
        generate_latest,
        CONTENT_TYPE_LATEST,
    )
else:

    class _Noop:
        def __call__(self, *a, **k):
            return self

        def labels(self, *a, **k):
            return self

        def observe(self, *a, **k):
            pass

        def inc(self, *a, **k):
            pass

    Counter = Histogram = _Noop  # type: ignore

    def generate_latest(*a, **k):
        return b""

    CONTENT_TYPE_LATEST = "text/plain"

from fastapi import APIRouter, Response


router = APIRouter()
requests_total = Counter(
    "idecide_requests_total", "Total HTTP requests", ["method", "path", "status"]
)
latency = Histogram("idecide_request_latency_seconds", "Request latency", ["path"])


@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
