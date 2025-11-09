from django.conf import settings
from django.dispatch import receiver
from constance import config
from constance.signals import config_updated
from django.core.signals import request_started

from karrio.server.core.logging import logger


def register_signals():
    config_updated.connect(constance_updated)
    # Defer config initialization until after Django is fully loaded
    request_started.connect(initialize_settings)

    logger.info("Signal registration complete", module="karrio.core")


def initialize_settings(sender=None, **kwargs):
    # Only run once
    if not getattr(initialize_settings, "has_run", False):
        try:
            update_settings(config)
            initialize_settings.has_run = True
        except Exception as e:
            logger.error("Failed to initialize settings", error=str(e))


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    update_settings(sender)


def update_settings(current):
    CONSTANCE_CONFIG_KEYS = [
        key for key in settings.CONSTANCE_CONFIG.keys() if hasattr(settings, key)
    ]

    for key in CONSTANCE_CONFIG_KEYS:
        try:
            setattr(settings, key, getattr(current, key))
        except Exception as e:
            logger.error("Failed to update setting", setting_key=key, error=str(e))

    # Check EMAIL_ENABLED after all settings are updated
    try:
        settings.EMAIL_ENABLED = all(
            cfg is not None and cfg != ""
            for cfg in [
                current.EMAIL_HOST,
                current.EMAIL_HOST_USER,
            ]
        )
    except Exception as e:
        logger.error("Failed to set EMAIL_ENABLED", error=str(e))
        settings.EMAIL_ENABLED = False
