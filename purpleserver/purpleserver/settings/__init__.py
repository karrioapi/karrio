__path__ = __import__('pkgutil').extend_path(__path__, __name__)  # type: ignore

import importlib.util
from purpleserver.settings.base import *
from purpleserver.settings.email import *
from purpleserver.settings.constance import *
from purpleserver.settings.tasks import *


if importlib.util.find_spec('purpleserver.graph') is not None:
    from purpleserver.settings.graph import *


if importlib.util.find_spec('purpleserver.orgs') is not None:
    from purpleserver.settings.orgs import *


""" Warning:: This section need to be last for settings extensibility """
if config('MULTI_TENANT_ENABLE', default=False, cast=bool):
    from purpleserver.settings.tenants import *

if importlib.util.find_spec('purpleserver.settings.main') is not None:
    from purpleserver.settings.main import *
