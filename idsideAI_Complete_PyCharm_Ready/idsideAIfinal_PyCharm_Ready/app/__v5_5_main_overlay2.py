try:
    from app.routers import telemetry_ui as telemetry_ui_router
    app.include_router(telemetry_ui_router.router)
except Exception:
    pass