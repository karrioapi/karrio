import logging
from huey import crontab
from django.conf import settings
from purpleserver.events.jobs import base, tracking

logger = logging.getLogger(__name__)
DEFAULT_TRACKERS_UPDATE_INTERVAL = getattr(settings, 'DEFAULT_TRACKERS_UPDATE_INTERVAL', 10800) / 60


@base.huey.periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
def trackers_update_job():
    tracking.update_trackers()
