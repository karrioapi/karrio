# type: ignore
"""
JTL Hub Main Settings Entrypoint

This is the main settings file for JTL Hub custom builds.
It imports base Karrio settings and extends them with JTL Hub-specific configuration.

To use this settings file:
    export DJANGO_SETTINGS_MODULE=karrio.server.settings.main
    # Or point to this file specifically from your wsgi/asgi files
"""

import importlib


if importlib.util.find_spec("karrio.server.shipping") is not None:
    from karrio.server.settings.shipping import *


if importlib.util.find_spec("karrio.server.admin") is not None:
    from karrio.server.settings.admin import *


if importlib.util.find_spec("karrio.server.orgs") is not None:
    from karrio.server.settings.orgs import *


if importlib.util.find_spec("karrio.server.audit") is not None:
    from karrio.server.settings.audit import *


if importlib.util.find_spec("karrio.server.automation") is not None:
    from karrio.server.settings.automation import *


if importlib.util.find_spec("karrio.server.apps") is not None:
    from karrio.server.settings.apps import *

# Import shipping module settings
if importlib.util.find_spec("karrio.server.shipping") is not None:
    from karrio.server.settings.shipping import *

# Import JTL Hub settings (must come after other modules to avoid being overridden)
if importlib.util.find_spec("karrio.server.jtl") is not None:
    from karrio.server.settings.jtl import *

# Warning: This section needs to be last for settings extensibility
if MULTI_TENANTS:
    from karrio.server.settings.tenants import *
