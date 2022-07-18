from django.db import connection
from django.conf import settings as base_settings

FEATURE_FLAGS = [
    "AUDIT_LOGGING",
    "ALLOW_SIGNUP",
    "ALLOW_ADMIN_APPROVED_SIGNUP",
    "ALLOW_MULTI_ACCOUNT",
    "ORDERS_MANAGEMENT",
    "APPS_MANAGEMENT",
    "DOCUMENTS_MANAGEMENT",
    "DATA_IMPORT_EXPORT",
    "CUSTOM_CARRIER_DEFINITION",
]
DEFAULT_ALLOWED_CONFIG = [
    "APP_NAME",
    "APP_WEBSITE",
    "SUPPORT_EMAIL",
    "BASE_TEMPLATE",
    "BASE_FOOTER_TEMPLATE",
]
FALLBACK_VALUES = {
    "APP_NAME": "Karrio",
    "SUPPORT_EMAIL": "hello@karrio.io",
    "BASE_TEMPLATE": "karrio/base_site.html",
    "BASE_FOOTER_TEMPLATE": "karrio/base_footer.html",
}


class _Settings:
    def __getattr__(self, item):
        if item == "tenant":
            return self._get_tenant()

        if item == "schema":
            return self._get_schema()

        if item == "APP_NAME":
            return getattr(self._get_tenant(), "name", FALLBACK_VALUES.get(item))

        if item in FEATURE_FLAGS and self._get_tenant() is not None:
            feature_flags = getattr(self._get_tenant(), "feature_flags", [])
            tenant_has_feature = item in feature_flags
            instance_has_feature = getattr(base_settings, item, False)
            return instance_has_feature and tenant_has_feature

        return getattr(base_settings, item, FALLBACK_VALUES.get(item))

    def _get_schema(self):
        return connection.get_schema() if base_settings.MULTI_TENANTS else None

    def _get_tenant(self):
        return connection.get_tenant() if base_settings.MULTI_TENANTS else None

    def get(self, item):
        return getattr(self, item)


settings = _Settings()
