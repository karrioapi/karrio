# type: ignore
from karrio.server.settings.base import *
import karrio.server.settings.constance as constance

JWT_APP_SECRET_KEY = config("JWT_APP_SECRET_KEY", default=SECRET_KEY)

# Extend middleware with app JWT authentication
core_auth_middleware = 'karrio.server.core.authentication.AuthenticationMiddleware'
app_middlewares = [
    'karrio.server.apps.middleware.AppJWTMiddleware',
    'karrio.server.apps.middleware.AppContextMiddleware',
]

try:
    # Find the index of the core authentication middleware to insert after
    index = next(i for i, m in enumerate(MIDDLEWARE) if core_auth_middleware in m)
    MIDDLEWARE = MIDDLEWARE[:index+1] + app_middlewares + MIDDLEWARE[index+1:]
except StopIteration:
    # Fallback in case core authentication middleware is not found
    MIDDLEWARE = app_middlewares + MIDDLEWARE
