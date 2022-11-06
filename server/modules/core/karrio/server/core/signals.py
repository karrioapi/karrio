import logging
from django.conf import settings
from django.dispatch import receiver

from constance.signals import config_updated

logger = logging.getLogger(__name__)


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    logger.info(f"Updated config {key} to {new_value}")
    update_settings(sender)


def update_settings(current):
    CONSTANCE_CONFIG_KEYS = [key for key in settings.CONSTANCE_CONFIG.keys() if hasattr(settings, "key")]

    for key in CONSTANCE_CONFIG_KEYS:
        setattr(settings, key, getattr(current, key))

    settings.EMAIL_ENABLED = all(
        cfg is not None and cfg != '' for cfg
        in [current.EMAIL_HOST, current.EMAIL_HOST_USER, current.EMAIL_HOST_PASSWORD]
    )
