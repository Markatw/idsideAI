# Auto-generated route imports for Sprint 24.9 stabilization
from .a11y_overlay import router as a11y_router
from .auth import router as auth_router
from .dashboard import router as dashboard_router
from .errors import router as errors_router
from .graph_tooltips import router as graph_tooltips_router
from .i18n import router as i18n_router
from .ui_theme import router as ui_theme_router

all_routers = [
    auth_router,
    dashboard_router,
    graph_tooltips_router,
    ui_theme_router,
    i18n_router,
    a11y_router,
    errors_router,
]
from . import db_crypto, dr, health, log_test, metrics, pii_crypto, probe, scim, slo, soak, sso
