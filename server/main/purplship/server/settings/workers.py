import os
import decouple
from huey import SqliteHuey
from karrio.server.settings import base as settings

# Karrio Server Background jobs interval config
DEFAULT_SCHEDULER_RUN_INTERVAL = 3600  # value is seconds. so 3600 seconds = 1 Hour
DEFAULT_TRACKERS_UPDATE_INTERVAL = decouple.config(
    "TRACKING_PULSE", default=7200, cast=int
)  # value is seconds. so 10800 seconds = 3 Hours


WORKER_DB_DIR = decouple.config("WORKER_DB_DIR", default=settings.WORK_DIR)
WORKER_DB_FILE_NAME = os.path.join(WORKER_DB_DIR, "tasks.sqlite3")
WORKER_IMMEDIATE_MODE = decouple.config("WORKER_IMMEDIATE_MODE", default=False)

settings.DATABASES["workers"] = {
    "NAME": WORKER_DB_FILE_NAME,
    "ENGINE": "django.db.backends.sqlite3",
}

HUEY = SqliteHuey(
    name="default",
    filename=WORKER_DB_FILE_NAME,
    **({"immediate": WORKER_IMMEDIATE_MODE} if WORKER_IMMEDIATE_MODE else {})
)
