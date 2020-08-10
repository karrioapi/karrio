from purpleserver.settings.base import *


MULTI_TENANT_ENABLE = bool(distutils.util.strtobool(os.environ.get('MULTI_TENANT_ENABLE', 'False')))


if MULTI_TENANT_ENABLE:
    from purpleserver.tenants.settings import *
