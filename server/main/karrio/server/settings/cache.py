from decouple import config
from karrio.server.settings.base import *
from karrio.server.settings.apm import HEALTH_CHECK_APPS


CACHE_TTL = 60 * 15
REDIS_HOST = config("REDIS_HOST", default=None)
REDIS_PORT = config("REDIS_PORT", default=None)

# karrio server caching setup
if REDIS_HOST is not None:
    HEALTH_CHECK_APPS += ["health_check.contrib.redis"]
    INSTALLED_APPS += ["health_check.contrib.redis"]

    REDIS_CONNECTION_URL = (
        f'redis://{REDIS_HOST or "127.0.0.1"}:{REDIS_PORT or "6379"}/1'
    )
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_CONNECTION_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "KEY_PREFIX": "karrio",
        }
    }
    print(f"Redis connection initialized at: {REDIS_CONNECTION_URL}")
