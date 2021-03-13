import logging
from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from django.conf import settings
from purpleserver.events.tasks import tracking

logger = logging.getLogger(__name__)
DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(settings, 'DEFAULT_TRACKERS_UPDATE_INTERVAL', 10800) / 60


@periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
def trackers_update_job():
    tracking.update_trackers()


@task()
def add(a, b):
    return a + b
