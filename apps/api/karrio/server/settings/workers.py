# type: ignore
import os
import huey
import redis
import decouple
from karrio.server.settings import base as settings


# Karrio Server Background jobs interval config
DEFAULT_SCHEDULER_RUN_INTERVAL = 3600  # value is seconds. so 3600 seconds = 1 Hour
DEFAULT_TRACKERS_UPDATE_INTERVAL = decouple.config(
    "TRACKING_PULSE", default=7200, cast=int
)  # value is seconds. so 10800 seconds = 3 Hours

WORKER_IMMEDIATE_MODE = decouple.config(
    "WORKER_IMMEDIATE_MODE", default=False, cast=bool
)

# Redis configuration - REDIS_URL takes precedence and supersedes granular env vars
REDIS_URL = decouple.config("REDIS_URL", default=None)

# Parse REDIS_URL or construct from individual parameters
if REDIS_URL is not None:
    from urllib.parse import urlparse

    parsed = urlparse(REDIS_URL)

    # Extract values from REDIS_URL (these supersede granular env vars)
    REDIS_HOST = parsed.hostname
    REDIS_PORT = parsed.port or 6379
    REDIS_USERNAME = parsed.username or "default"
    REDIS_PASSWORD = parsed.password

    # Determine SSL from URL scheme (rediss:// means SSL is enabled)
    REDIS_SCHEME = parsed.scheme if parsed.scheme in ("redis", "rediss") else "redis"
    REDIS_SSL = REDIS_SCHEME == "rediss"

else:
    # Fall back to individual parameters
    REDIS_HOST = decouple.config("REDIS_HOST", default=None)
    REDIS_PORT = decouple.config("REDIS_PORT", default=None)
    REDIS_PASSWORD = decouple.config("REDIS_PASSWORD", default=None)
    REDIS_USERNAME = decouple.config("REDIS_USERNAME", default="default")
    REDIS_SSL = decouple.config("REDIS_SSL", default=False, cast=bool)

# Configure HUEY based on available Redis configuration
if REDIS_HOST is not None:
    pool = redis.ConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        max_connections=20,
        **({"ssl": REDIS_SSL} if REDIS_SSL else {}),
        **({"password": REDIS_PASSWORD} if REDIS_PASSWORD else {}),
        **({"username": REDIS_USERNAME} if REDIS_USERNAME else {}),
    )
    HUEY = huey.RedisHuey(
        "default",
        connection_pool=pool,
        **({"immediate": WORKER_IMMEDIATE_MODE} if WORKER_IMMEDIATE_MODE else {}),
    )

else:
    # No Redis configured, use SQLite
    WORKER_DB_DIR = decouple.config("WORKER_DB_DIR", default=settings.WORK_DIR)
    WORKER_DB_FILE_NAME = os.path.join(WORKER_DB_DIR, "tasks.sqlite3")

    settings.DATABASES["workers"] = {
        "NAME": WORKER_DB_FILE_NAME,
        "ENGINE": "django.db.backends.sqlite3",
    }

    HUEY = huey.SqliteHuey(
        name="default",
        filename=WORKER_DB_FILE_NAME,
        **({"immediate": WORKER_IMMEDIATE_MODE} if WORKER_IMMEDIATE_MODE else {}),
    )
