from django.conf import settings
from django.dispatch import receiver
from constance import config
from constance.signals import config_updated
from django.core.signals import request_started

from karrio.server.core.logging import logger


def register_signals():
    config_updated.connect(constance_updated)
    request_started.connect(initialize_settings)

    logger.info("Signal registration complete", module="karrio.core")


def initialize_settings(_sender=None, **_kwargs):
    """Initialize Django settings from constance on first request."""
    if getattr(initialize_settings, "has_run", False):
        return

    try:
        update_settings(config)
        initialize_settings.has_run = True
    except Exception as e:
        logger.error("Failed to initialize settings", error=str(e))


@receiver(config_updated)
def constance_updated(sender, **_kwargs):
    update_settings(sender)


def update_settings(current):
    """Sync constance values to Django settings."""
    keys = [k for k in settings.CONSTANCE_CONFIG.keys() if hasattr(settings, k)]

    for key in keys:
        try:
            setattr(settings, key, getattr(current, key))
        except Exception:
            pass  # Ignore errors during test/initialization when constance table may not exist

    # Update EMAIL_ENABLED based on email config
    try:
        settings.EMAIL_ENABLED = all(
            cfg not in (None, "")
            for cfg in [current.EMAIL_HOST, current.EMAIL_HOST_USER]
        )
    except Exception:
        settings.EMAIL_ENABLED = False
