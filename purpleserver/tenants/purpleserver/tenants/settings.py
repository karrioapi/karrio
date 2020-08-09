from purpleserver.settings.base import (
    DATABASES,
    MIDDLEWARE,
    DJANGO_APPS,
    INSTALLED_APPS
)

DATABASES["default"]["ENGINE"] = "tenant_schemas.postgresql_backend"

MIDDLEWARE = [
    'tenant_schemas.middleware.TenantMiddleware',
    *MIDDLEWARE,
]

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

SHARED_APPS = [
    "tenant_schemas",
    "purpleserver.tenants",

    *DJANGO_APPS
]

TENANT_APPS = [*INSTALLED_APPS]

INSTALLED_APPS = [
    "tenant_schemas",
    "purpleserver.tenants",

    *INSTALLED_APPS
]

PUBLIC_SCHEMA_NAME = 'public'
TENANT_MODEL = "tenants.Client"
DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'
TENANT_LIMIT_SET_CALLS = True
PUBLIC_SCHEMA_URLCONF = 'purpleserver.tenants.urls'
