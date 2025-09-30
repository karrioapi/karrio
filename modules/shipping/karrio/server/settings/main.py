# type: ignore
import importlib


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


if importlib.util.find_spec("karrio.server.shipping") is not None:
    from karrio.server.settings.shipping import *


""" Warning:: This section need to be last for settings extensibility """
if MULTI_TENANTS:
    from karrio.server.settings.tenants import *
