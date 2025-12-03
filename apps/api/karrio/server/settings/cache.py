# type: ignore
import sys
from decouple import config
from karrio.server.settings.base import *
from karrio.server.settings.apm import HEALTH_CHECK_APPS
from karrio.server.core.logging import logger


CACHE_TTL = 60 * 15

# Check if worker is running in detached mode (separate from API server)
DETACHED_WORKER = config("DETACHED_WORKER", default=False, cast=bool)

# Detect if running as a worker process (via run_huey command)
IS_WORKER_PROCESS = any("run_huey" in arg for arg in sys.argv)

# Skip default Redis cache configuration only for worker processes
# API servers should use Redis cache even when DETACHED_WORKER is True
SKIP_DEFAULT_CACHE = IS_WORKER_PROCESS

# Redis configuration - REDIS_URL takes precedence and supersedes granular env vars
REDIS_URL = config("REDIS_URL", default=None)
REDIS_PREFIX = config("REDIS_PREFIX", default="karrio")
REDIS_SSL = config("REDIS_SSL", default=False, cast=bool)

# Parse REDIS_URL or construct from individual parameters
if REDIS_URL is not None:
    from urllib.parse import urlparse, urlunparse
    import re

    parsed = urlparse(REDIS_URL)

    # Extract values from REDIS_URL (these supersede granular env vars)
    REDIS_HOST = parsed.hostname
    REDIS_PORT = parsed.port or 6379
    REDIS_USERNAME = parsed.username or "default"
    REDIS_PASSWORD = parsed.password

    # Determine SSL from URL scheme (rediss:// means SSL is enabled)
    REDIS_SCHEME = parsed.scheme if parsed.scheme in ("redis", "rediss") else "redis"
    REDIS_SSL = REDIS_SCHEME == "rediss"

    # Build connection URL with database 1 for cache
    REDIS_AUTH = f"{REDIS_USERNAME}:{REDIS_PASSWORD}@" if REDIS_PASSWORD else ""
    REDIS_CONNECTION_URL = f"{REDIS_SCHEME}://{REDIS_AUTH}{REDIS_HOST}:{REDIS_PORT}/1"

else:
    # Fall back to individual parameters
    REDIS_HOST = config("REDIS_HOST", default=None)
    REDIS_PORT = config("REDIS_PORT", default=None)
    REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
    REDIS_USERNAME = config("REDIS_USERNAME", default="default")

    if REDIS_HOST is not None:
        REDIS_AUTH = f"{REDIS_USERNAME}:{REDIS_PASSWORD}@" if REDIS_PASSWORD else ""
        REDIS_SCHEME = "rediss" if REDIS_SSL else "redis"
        REDIS_CONNECTION_URL = (
            f'{REDIS_SCHEME}://{REDIS_AUTH}{REDIS_HOST}:{REDIS_PORT or "6379"}/1'
        )

# Configure Django cache if Redis is available and not in worker mode
if REDIS_HOST is not None and not SKIP_DEFAULT_CACHE:
    # Configure connection pool with max_connections to prevent exhaustion
    # Default: 50 connections per process (2 Gunicorn workers = 100 total)
    # Azure Redis Basic: 256 max connections total
    REDIS_CACHE_MAX_CONNECTIONS = config(
        "REDIS_CACHE_MAX_CONNECTIONS", default=50, cast=int
    )

    pool_kwargs = {"max_connections": REDIS_CACHE_MAX_CONNECTIONS}
    if REDIS_SSL:
        pool_kwargs["ssl_cert_reqs"] = None

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_CONNECTION_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                **(
                    {"CONNECTION_POOL_KWARGS": {"ssl_cert_reqs": None}}
                    if REDIS_SSL
                    else {}
                ),
            },
            "KEY_PREFIX": REDIS_PREFIX,
        }
    }

    # Cache constance values to avoid N+1 queries on each config access
    CONSTANCE_DATABASE_CACHE_BACKEND = "default"

    # Django cache health check uses the cache backend directly
    # Only add Redis health check if REDIS_URL environment variable is set
    # When using granular params, the cache check is sufficient
    if config("REDIS_URL", default=None) is not None:
        HEALTH_CHECK_APPS += ["health_check.contrib.redis"]
        INSTALLED_APPS += ["health_check.contrib.redis"]

    print(f"Redis cache connection initialized")
elif SKIP_DEFAULT_CACHE:
    print(
        "Skipping default Redis cache configuration (worker mode - only HUEY Redis needed)"
    )
