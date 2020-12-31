__path__ = __import__('pkgutil').extend_path(__path__, __name__)  # type: ignore

from decouple import config
from purpleserver.settings.base import *
from purpleserver.settings.email import *
from purpleserver.settings.constance import *

if config('MULTI_TENANT_ENABLE', default=False, cast=bool):
    from purpleserver.settings.tenants import *
