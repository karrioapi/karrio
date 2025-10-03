# type: ignore
from karrio.server.settings.base import *
import karrio.server.settings.constance as constance

INSTALLED_APPS += [
    "karrio.server.admin",
]
KARRIO_URLS += [
    "karrio.server.admin.urls",
]

## White label settings

APP_NAME = config("APP_NAME", default="Karrio")
APP_WEBSITE = config("APP_WEBSITE", default="https://karrio.io")

CONSTANCE_CONFIG = {
    "APP_NAME": (APP_NAME, "The name of the application", str),
    "APP_WEBSITE": (APP_WEBSITE, "The website of the application", str),
    **constance.CONSTANCE_CONFIG,
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Platform Config": ("APP_NAME", "APP_WEBSITE"),
    **constance.CONSTANCE_CONFIG_FIELDSETS,
}
