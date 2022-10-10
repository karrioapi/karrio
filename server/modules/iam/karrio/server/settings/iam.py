# type: ignore
from karrio.server.settings.base import *

INSTALLED_APPS += ["karrio.server.iam"]

PERMISSION_CHECKS += ["karrio.server.iam.permissions.check_context_permissions"]
