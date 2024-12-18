# type: ignore
from decouple import config
from karrio.server.settings.base import *
from karrio.server.settings.apm import HEALTH_CHECK_APPS


CACHE_TTL = 60 * 15
REDIS_HOST = config("REDIS_HOST", default=None)
REDIS_PORT = config("REDIS_PORT", default=None)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
REDIS_USERNAME = config("REDIS_USERNAME", default="default")
REDIS_PREFIX = config("REDIS_PREFIX", default="karrio")

# karrio server caching setup
if REDIS_HOST is not None:
    HEALTH_CHECK_APPS += ["health_check.contrib.redis"]
    INSTALLED_APPS += ["health_check.contrib.redis"]
    REDIS_AUTH = f"{REDIS_USERNAME}:{REDIS_PASSWORD}@" if REDIS_PASSWORD else ""

    REDIS_CONNECTION_URL = f'redis://{REDIS_AUTH}{REDIS_HOST}:{REDIS_PORT or "6379"}/1'
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_CONNECTION_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "KEY_PREFIX": REDIS_PREFIX,
        }
    }
    print(f"Redis connection initialized at: {REDIS_CONNECTION_URL}")
