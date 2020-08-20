__path__ = __import__('pkgutil').extend_path(__path__, __name__)  # type: ignore

from purpleserver.settings.base import *

if config('MULTI_TENANT_ENABLE', default=False, cast=bool):
    from purpleserver.settings.tenants import *
