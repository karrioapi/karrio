# type: ignore
from karrio.server.settings.base import *
from karrio.server.settings.constance import *

## White label settings

APP_NAME = config("APP_NAME", default="JTL Shipping")
APP_WEBSITE = config("APP_WEBSITE", default="https://jtl-software.de")


CONSTANCE_CONFIG = {
    "APP_NAME": (APP_NAME, "The name of the application", str),
    "APP_WEBSITE": (APP_WEBSITE, "The website of the application", str),
    **CONSTANCE_CONFIG,
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Platform Config": ("APP_NAME", "APP_WEBSITE"),
    **CONSTANCE_CONFIG_FIELDSETS,
}

# Extend authentication classes with JTL JWT authentication (prepend to list)
AUTHENTICATION_CLASSES = [
    "karrio.server.jtl.authentication.JTLJWTAuthentication",
    *AUTHENTICATION_CLASSES,
]
KARRIO_URLS += ["karrio.server.jtl.urls"]
INSTALLED_APPS += ["karrio.server.jtl"]

# JTL JWT Configuration
# JWT_SECRET is used for symmetric HS256 encryption/decryption
JWT_SECRET = config(
    "JWT_SECRET",
    default=""
)

# Logging configuration for JTL
LOGGING["loggers"]["karrio.server.jtl"] = {
    "handlers": ["file", "console"],
    "level": LOG_LEVEL,
    "propagate": False,
}
