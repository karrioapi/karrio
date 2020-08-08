from purpleserver.settings.base import (
    DATABASES,
    MIDDLEWARE,
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

SHARED_APPS = ["tenant_schemas", "purpleserver.tenants"]

TENANT_APPS = INSTALLED_APPS

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

TENANT_MODEL = "tenants.Client"
DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'
