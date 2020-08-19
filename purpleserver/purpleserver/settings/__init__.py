__path__ = __import__('pkgutil').extend_path(__path__, __name__)  # type: ignore

from purpleserver.settings.base import *


MULTI_TENANT_ENABLE = bool(distutils.util.strtobool(os.environ.get('MULTI_TENANT_ENABLE', 'False')))


if MULTI_TENANT_ENABLE:
    from purpleserver.settings.tenants import *
