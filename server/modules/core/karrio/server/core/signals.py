import logging
from django.dispatch import receiver
from django.conf import settings

from constance.signals import config_updated

logger = logging.getLogger(__name__)


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    logger.info(f"Updated config {key} to {new_value}")
    update_settings(sender)


def update_settings(current):
    settings.EMAIL_USE_TLS = current.EMAIL_USE_TLS
    settings.EMAIL_HOST_USER = current.EMAIL_HOST_USER
    settings.EMAIL_HOST_PASSWORD = current.EMAIL_HOST_PASSWORD
    settings.EMAIL_HOST = current.EMAIL_HOST
    settings.EMAIL_PORT = current.EMAIL_PORT
    settings.EMAIL_FROM_ADDRESS = current.EMAIL_FROM_ADDRESS

    settings.EMAIL_SERVER = current.EMAIL_HOST
    settings.EMAIL_ADDRESS = current.EMAIL_HOST_USER
    settings.EMAIL_PASSWORD = current.EMAIL_HOST_PASSWORD
    settings.EMAIL_ENABLED = all(
        cfg is not None and cfg != '' for cfg in [current.EMAIL_HOST, current.EMAIL_HOST_USER, current.EMAIL_HOST_PASSWORD]
    )

    settings.GOOGLE_CLOUD_API_KEY = current.GOOGLE_CLOUD_API_KEY
    settings.CANADAPOST_ADDRESS_COMPLETE_API_KEY = current.CANADAPOST_ADDRESS_COMPLETE_API_KEY
