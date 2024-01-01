# type: ignore
import posthog
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from posthog.sentry.posthog_integration import PostHogIntegration
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


# PostHog
POSTHOG_KEY = config("POSTHOG_KEY", default=None)
POSTHOG_HOST = config("POSTHOG_HOST", default="https://app.posthog.com")

if POSTHOG_KEY:
    posthog.project_api_key = POSTHOG_KEY
    posthog.host = POSTHOG_HOST


#  Sentry
sentry_sdk.utils.MAX_STRING_LENGTH = 4096
SENTRY_DSN = config("SENTRY_DSN", default=None)

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=(
            [DjangoIntegration(), PostHogIntegration()]
            if POSTHOG_KEY
            else [DjangoIntegration()]
        ),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
