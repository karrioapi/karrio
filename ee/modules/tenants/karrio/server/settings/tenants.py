# type: ignore
from django.conf.global_settings import CACHES
from karrio.server.settings.base import *
from karrio.server.settings.cache import HEALTH_CHECK_APPS


DATABASES["default"]["ENGINE"] = "django_tenants.postgresql_backend"

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    *MIDDLEWARE,
]

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

SHARED_APPS = [
    "constance",
    "django_tenants",
    "karrio.server.tenants",
    *BASE_APPS,
    "constance.backends.database",
    *HEALTH_CHECK_APPS,
    *OTP_APPS,
]

EXCLUDED_TENANT_APPS = ["constance", "constance.backends.database"]

TENANT_APPS = [app for app in INSTALLED_APPS if app not in EXCLUDED_TENANT_APPS]

INSTALLED_APPS = ["django_tenants", "karrio.server.tenants", *INSTALLED_APPS]

TENANT_MODEL = "tenants.Client"  # app.Model
TENANT_DOMAIN_MODEL = "tenants.Domain"  # app.Model

PUBLIC_SCHEMA_NAME = "public"
PUBLIC_SCHEMA_URLCONF = "karrio.server.tenants.urls"
TENANT_LIMIT_SET_CALLS = True
TENANT_COLOR_ADMIN_APPS = False
TENANT_ADMIN_API_URLS = []

# Cache config
CACHES["default"]["KEY_FUNCTION"] = "django_tenants.cache.make_key"
CACHES["default"]["REVERSE_KEY_FUNCTION"] = "django_tenants.cache.reverse_key"
