import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from karrio.server.settings.base import *


# Health check apps settings
HEALTH_CHECK_APPS = [
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",
]
INSTALLED_APPS += HEALTH_CHECK_APPS

#  Sentry
sentry_sdk.utils.MAX_STRING_LENGTH = 4096
SENTRY_DSN = config("SENTRY_DSN", default=None)

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
