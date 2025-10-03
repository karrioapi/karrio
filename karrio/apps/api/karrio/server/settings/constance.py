""" Dynamic configuration editable on runtime powered by django-constance."""

from decouple import config
import karrio.references as ref
import karrio.server.settings.base as base
from karrio.server.settings.email import (
    EMAIL_USE_TLS,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_FROM_ADDRESS,
)
import importlib.util

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

# registry config
ENABLE_ALL_PLUGINS_BY_DEFAULT = config("ENABLE_ALL_PLUGINS_BY_DEFAULT", default=True if base.DEBUG else False, cast=bool)

# Create feature flags config only for modules that exist
FEATURE_FLAGS_CONFIG = {
    "AUDIT_LOGGING": (
        (
            base.AUDIT_LOGGING,
            "Audit logging",
            bool,
        )
        if importlib.util.find_spec("karrio.server.audit") is not None
        else None
    ),
    "ALLOW_SIGNUP": (
        base.ALLOW_SIGNUP,
        "Allow signup",
        bool,
    ),
    "ALLOW_ADMIN_APPROVED_SIGNUP": (
        base.ALLOW_ADMIN_APPROVED_SIGNUP,
        "Allow admin approved signup",
        bool,
    ),
    "ALLOW_MULTI_ACCOUNT": (
        base.ALLOW_MULTI_ACCOUNT,
        "Allow multi account",
        bool,
    ),
    "ADMIN_DASHBOARD": (
        (
            base.ADMIN_DASHBOARD,
            "Admin dashboard",
            bool,
        )
        if importlib.util.find_spec("karrio.server.admin") is not None
        else None
    ),
    "MULTI_ORGANIZATIONS": (
        (
            base.MULTI_ORGANIZATIONS,
            "Multi organizations",
            bool,
        )
        if importlib.util.find_spec("karrio.server.orgs") is not None
        else None
    ),
    "ORDERS_MANAGEMENT": (
        (
            base.ORDERS_MANAGEMENT,
            "Orders management",
            bool,
        )
        if importlib.util.find_spec("karrio.server.orders") is not None
        else None
    ),
    "APPS_MANAGEMENT": (
        (
            base.APPS_MANAGEMENT,
            "Apps management",
            bool,
        )
        if importlib.util.find_spec("karrio.server.apps") is not None
        else None
    ),
    "DOCUMENTS_MANAGEMENT": (
        (
            base.DOCUMENTS_MANAGEMENT,
            "Documents management",
            bool,
        )
        if importlib.util.find_spec("karrio.server.documents") is not None
        else None
    ),
    "DATA_IMPORT_EXPORT": (
        (
            base.DATA_IMPORT_EXPORT,
            "Data import export",
            bool,
        )
        if importlib.util.find_spec("karrio.server.data") is not None
        else None
    ),
    "WORKFLOW_MANAGEMENT": (
        (
            base.WORKFLOW_MANAGEMENT,
            "Workflow management",
            bool,
        )
        if importlib.util.find_spec("karrio.server.automation") is not None
        else None
    ),
    "SHIPPING_RULES": (
        (
            base.SHIPPING_RULES,
            "Shipping rules",
            bool,
        )
        if importlib.util.find_spec("karrio.server.automation") is not None
        else None
    ),
    "ADVANCED_ANALYTICS": (
        (
            base.ADVANCED_ANALYTICS,
            "Advanced analytics",
            bool,
        )
        if importlib.util.find_spec("karrio.server.analytics") is not None
        else None
    ),
    "PERSIST_SDK_TRACING": (
        base.PERSIST_SDK_TRACING,
        "Persist SDK tracing",
        bool,
    ),
}

# Update fieldsets to only include existing feature flags
FEATURE_FLAGS_FIELDSET = [k for k, v in FEATURE_FLAGS_CONFIG.items() if v is not None]

# Plugin registry
ref.collect_failed_plugins_data()
PLUGIN_REGISTRY = {
    "ENABLE_ALL_PLUGINS_BY_DEFAULT": (
        ENABLE_ALL_PLUGINS_BY_DEFAULT,
        "Enable all plugins by default",
        bool,
    ),
    **{
        f"{ext.upper()}_ENABLED": (
            config(f"{ext.upper()}_ENABLED", default=True, cast=bool),
            f"{metadata.get('label')} plugin",
            bool,
        ) for ext, metadata in ref.PLUGIN_METADATA.items()
    }
}


# Filter out None values and update CONSTANCE_CONFIG
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
        "Trackers data retention period (in days)",
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
    **{k: v for k, v in FEATURE_FLAGS_CONFIG.items() if v is not None},
    **PLUGIN_REGISTRY,
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
    "Data Retention": (
        "ORDER_DATA_RETENTION",
        "TRACKER_DATA_RETENTION",
        "SHIPMENT_DATA_RETENTION",
        "API_LOGS_DATA_RETENTION",
    ),
    "Feature Flags": tuple(FEATURE_FLAGS_FIELDSET),
    "Registry Config": ("ENABLE_ALL_PLUGINS_BY_DEFAULT",),
    "Registry Plugins": tuple([k for k in PLUGIN_REGISTRY.keys() if not k in ("ENABLE_ALL_PLUGINS_BY_DEFAULT",)]),
}
