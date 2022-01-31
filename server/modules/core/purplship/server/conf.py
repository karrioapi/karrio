from django.db import connection
from django.conf import settings as base_settings

DEFAULT_ALLOWED_CONFIG = [
    "APP_NAME",
    "APP_WEBSITE",
    "SUPPORT_EMAIL",
    "BASE_TEMPLATE",
    "BASE_FOOTER_TEMPLATE",
]
FALLBACK_VALUES = {
    "APP_NAME": "Purplship",
    "APP_WEBSITE": "https://purplship.com",
    "SUPPORT_EMAIL": "hello@purplship.com",
    "BASE_TEMPLATE": "purplship/base_site.html",
    "BASE_FOOTER_TEMPLATE": "purplship/base_footer.html",
}


class Settings:
    def __init__(self):
        self.tenant = connection.get_tenant() if base_settings.MULTI_TENANTS else None

    def __getattr__(self, item):
        if item == "APP_NAME":
            return getattr(self.tenant, "name", FALLBACK_VALUES.get(item))

        return getattr(base_settings, item, FALLBACK_VALUES.get(item))

    def get(self, item, tenant=None):
        if tenant:
            self.tenant = tenant

        return getattr(self, item)


settings = Settings()
