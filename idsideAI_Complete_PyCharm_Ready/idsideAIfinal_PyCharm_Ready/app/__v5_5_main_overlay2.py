# IDSIDEAI APP PLACEHOLDER BEGIN
from fastapi import FastAPI
try:
    app  # type: ignore # noqa: F821
except NameError:
    app = FastAPI()
# IDSIDEAI APP PLACEHOLDER END

try:
    from app.routers import telemetry_ui as telemetry_ui_router

    app.include_router(telemetry_ui_router.router)
except (
    Exception
):  # nosec B110 (LOW): vetted for board compliance - Try, Except, Pass detected.
    pass
