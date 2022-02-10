__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

import importlib.util
from purplship.server.settings.base import *
from purplship.server.settings.email import *
from purplship.server.settings.constance import *
from purplship.server.settings.workers import *
from purplship.server.settings.cache import *


if importlib.util.find_spec("purplship.server.graph") is not None:
    from purplship.server.settings.graph import *


if importlib.util.find_spec("purplship.server.orders") is not None:
    from purplship.server.settings.orders import *


if importlib.util.find_spec("purplship.server.orgs") is not None:
    from purplship.server.settings.orgs import *


""" Warning:: This section need to be last for settings extensibility """
if MULTI_TENANTS:
    from purplship.server.settings.tenants import *

if importlib.util.find_spec("purplship.server.settings.main") is not None:
    from purplship.server.settings.main import *
