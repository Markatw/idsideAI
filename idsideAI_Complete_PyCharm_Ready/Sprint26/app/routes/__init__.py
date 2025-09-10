# Auto-generated route imports for Sprint 24.9 stabilization
from .auth import router as auth_router
from .dashboard import router as dashboard_router
from .graph_tooltips import router as graph_tooltips_router
from .ui_theme import router as ui_theme_router
from .i18n import router as i18n_router
from .a11y_overlay import router as a11y_router
from .errors import router as errors_router

all_routers = [
    auth_router,
    dashboard_router,
    graph_tooltips_router,
    ui_theme_router,
    i18n_router,
    a11y_router,
    errors_router,
]
from . import scim
from . import sso
from . import pii_crypto
from . import db_crypto
from . import dr
from . import metrics
from . import log_test

from . import soak
from . import slo
from . import probe

from . import health
