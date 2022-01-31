from pprint import pprint
from django.conf.global_settings import CACHES
from purplship.server.settings.base import *


DATABASES["default"]["ENGINE"] = "django_tenants.postgresql_backend"

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    *MIDDLEWARE,
]

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

SHARED_APPS = [
    "constance",
    "django_tenants",
    "purplship.server.tenants",
    *BASE_APPS,
    "constance.backends.database",
]

EXCLUDED_TENANT_APPS = ["constance", "constance.backends.database"]

TENANT_APPS = [app for app in INSTALLED_APPS if app not in EXCLUDED_TENANT_APPS]

INSTALLED_APPS = ["django_tenants", "purplship.server.tenants", *INSTALLED_APPS]


TENANT_MODEL = "tenants.Client"  # app.Model
TENANT_DOMAIN_MODEL = "tenants.Domain"  # app.Model

PUBLIC_SCHEMA_NAME = "public"
PUBLIC_SCHEMA_URLCONF = "purplship.server.tenants.urls"
TENANT_LIMIT_SET_CALLS = True
TENANT_COLOR_ADMIN_APPS = False

# Storage config
MEDIA_ROOT = BASE_DIR / "/media"
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "django_tenants.storage.TenantFileSystemStorage"

# Cache config
CACHES["default"]["KEY_FUNCTION"] = "django_tenants.cache.make_key"
CACHES["default"]["REVERSE_KEY_FUNCTION"] = "django_tenants.cache.reverse_key"
