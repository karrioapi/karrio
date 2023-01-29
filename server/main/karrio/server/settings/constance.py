""" Dynamic configuration editable on runtime powered by django-constance."""
from decouple import config
from karrio.server.settings.email import (
    EMAIL_USE_TLS,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_FROM_ADDRESS,
)

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_DATABASE_PREFIX = "constance:core:"
DATA_ARCHIVING_SCHEDULE = config("DATA_ARCHIVING_SCHEDULE", default=168, cast=int)

GOOGLE_CLOUD_API_KEY = config("GOOGLE_CLOUD_API_KEY", default="")
CANADAPOST_ADDRESS_COMPLETE_API_KEY = config(
    "CANADAPOST_ADDRESS_COMPLETE_API_KEY", default=""
)
# data retention env in days
ORDER_DATA_RETENTION = config("ORDER_DATA_RETENTION", default=183, cast=int)
TRACKER_DATA_RETENTION = config("TRACKER_DATA_RETENTION", default=183, cast=int)
SHIPMENT_DATA_RETENTION = config("SHIPMENT_DATA_RETENTION", default=183, cast=int)
API_LOGS_DATA_RETENTION = config("API_LOGS_DATA_RETENTION", default=92, cast=int)

CONSTANCE_CONFIG = {
    "EMAIL_USE_TLS": (
        EMAIL_USE_TLS,
        "Determine whether the configuration support TLS",
        bool,
    ),
    "EMAIL_HOST_USER": (
        EMAIL_HOST_USER,
        "The authentication user (email). e.g: admin@karrio.io",
        str,
    ),
    "EMAIL_HOST_PASSWORD": (EMAIL_HOST_PASSWORD, "The authentication password", str),
    "EMAIL_HOST": (EMAIL_HOST, "The mail server host. e.g: smtp.gmail.com", str),
    "EMAIL_PORT": (
        EMAIL_PORT,
        "The mail server port. e.g: 465 (SSL required) or 587 (TLS required)",
        int,
    ),
    "EMAIL_FROM_ADDRESS": (
        EMAIL_FROM_ADDRESS,
        "Email sent from. e.g: noreply@karrio.io",
        str,
    ),
    "GOOGLE_CLOUD_API_KEY": (GOOGLE_CLOUD_API_KEY, "A Google GeoCoding API key", str),
    "CANADAPOST_ADDRESS_COMPLETE_API_KEY": (
        CANADAPOST_ADDRESS_COMPLETE_API_KEY,
        "The Canada Post AddressComplete service API Key",
        str,
    ),
    "ORDER_DATA_RETENTION": (
        ORDER_DATA_RETENTION,
        "Order data retention period (in days)",
        int,
    ),
    "TRACKER_DATA_RETENTION": (
        TRACKER_DATA_RETENTION,
        "Order data retention period (in days)",
        int,
    ),
    "SHIPMENT_DATA_RETENTION": (
        SHIPMENT_DATA_RETENTION,
        "Shipment data retention period (in days)",
        int,
    ),
    "API_LOGS_DATA_RETENTION": (
        API_LOGS_DATA_RETENTION,
        "API request and SDK tracing logs retention period (in days)",
        int,
    ),
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Email Config": (
        "EMAIL_USE_TLS",
        "EMAIL_HOST_USER",
        "EMAIL_HOST_PASSWORD",
        "EMAIL_HOST",
        "EMAIL_PORT",
        "EMAIL_FROM_ADDRESS",
    ),
    "Address Validation Service": (
        "GOOGLE_CLOUD_API_KEY",
        "CANADAPOST_ADDRESS_COMPLETE_API_KEY",
    ),
    "Data retention": (
        "ORDER_DATA_RETENTION",
        "TRACKER_DATA_RETENTION",
        "SHIPMENT_DATA_RETENTION",
        "API_LOGS_DATA_RETENTION",
    ),
}
