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

REDIS_HOST = decouple.config("REDIS_HOST", default=None)
REDIS_PORT = decouple.config("REDIS_PORT", default=None)


# Use redis if available
if REDIS_HOST is not None:
    pool = redis.ConnectionPool(
        host=REDIS_HOST, port=REDIS_PORT or "6379", max_connections=20
    )
    HUEY = huey.RedisHuey(
        "default",
        connection_pool=pool,
        **({"immediate": WORKER_IMMEDIATE_MODE} if WORKER_IMMEDIATE_MODE else {})
    )

else:
    WORKER_DB_DIR = decouple.config("WORKER_DB_DIR", default=settings.WORK_DIR)
    WORKER_DB_FILE_NAME = os.path.join(WORKER_DB_DIR, "tasks.sqlite3")

    settings.DATABASES["workers"] = {
        "NAME": WORKER_DB_FILE_NAME,
        "ENGINE": "django.db.backends.sqlite3",
    }

    HUEY = huey.SqliteHuey(
        name="default",
        filename=WORKER_DB_FILE_NAME,
        **({"immediate": WORKER_IMMEDIATE_MODE} if WORKER_IMMEDIATE_MODE else {})
    )
