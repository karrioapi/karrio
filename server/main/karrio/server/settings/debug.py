import importlib.util
from karrio.server.settings.base import *


if DEBUG and importlib.util.find_spec("debug_toolbar") is not None:
    INTERNAL_IPS = [
        "127.0.0.1",
        "0.0.0.0",
    ]
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE.insert(0, "karrio.server.core.middleware.NonHtmlDebugToolbarMiddleware")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
