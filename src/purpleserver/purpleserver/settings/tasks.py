import os
import decouple
from purpleserver.settings import base as settings

# Purplship Server Background jobs interval config
DEFAULT_SCHEDULER_RUN_INTERVAL = 3600  # value is seconds. so 3600 seconds = 1 Hour
DEFAULT_TRACKERS_UPDATE_INTERVAL = 10800  # value is seconds. so 10800 seconds = 3 Hours


TASKS_DB_DIR = decouple.config('TASKS_DB_DIR', default=settings.WORK_DIR)
TASKS_DB_FILE_NAME = os.path.join(TASKS_DB_DIR, 'tasks.sqlite3')


DATABASES = {
    **settings.DATABASES,
    'tasks': {
        'NAME': TASKS_DB_FILE_NAME,
        'ENGINE': 'django.db.backends.sqlite3',
    }
}


HUEY = {
    'name': 'purpleserver',
    'huey_class': 'huey.SqliteHuey',  # Huey implementation to use.
    'filename': TASKS_DB_FILE_NAME,
    'immediate': False,  # If DEBUG=True, run synchronously.
    'utc': True,  # Use UTC for all times internally.
    'fsync': True,
    'consumer': {
        'blocking': True,  # Use blocking list pop instead of polling Redis.
        'loglevel': settings.LOG_LEVEL,
        'workers': 1,
        'scheduler_interval': 1,
        'simple_log': True,
        'periodic': True,  # Enable crontab feature.
    },
}
