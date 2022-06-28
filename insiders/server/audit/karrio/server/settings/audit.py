# type: ignore
from karrio.server.settings.base import *


INSTALLED_APPS += ["auditlog", "karrio.server.audit"]

MIDDLEWARE = [
    *MIDDLEWARE,
    "karrio.server.audit.middleware.AuditLogMiddleware",
]

MODEL_TRANSFORMERS = [*MODEL_TRANSFORMERS, "karrio.server.audit.hooks.register_model"]

AUDITLOG_INCLUDE_ALL_MODELS = False
