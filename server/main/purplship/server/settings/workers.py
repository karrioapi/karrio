import os
import decouple
from huey import SqliteHuey
from purplship.server.settings import base as settings

# Purplship Server Background jobs interval config
DEFAULT_SCHEDULER_RUN_INTERVAL = 3600  # value is seconds. so 3600 seconds = 1 Hour
DEFAULT_TRACKERS_UPDATE_INTERVAL = 10800  # value is seconds. so 10800 seconds = 3 Hours


WORKER_DB_DIR = decouple.config('WORKER_DB_DIR', default=settings.WORK_DIR)
WORKER_DB_FILE_NAME = os.path.join(WORKER_DB_DIR, 'tasks.sqlite3')

settings.DATABASES['workers'] = {
    'NAME': WORKER_DB_FILE_NAME,
    'ENGINE': 'django.db.backends.sqlite3',
}

HUEY = SqliteHuey(
    name='default',
    filename=WORKER_DB_FILE_NAME
)
