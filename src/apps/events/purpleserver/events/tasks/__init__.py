import logging
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task
from purpleserver.events.tasks import tracking, webhook

logger = logging.getLogger(__name__)
DEFAULT_TRACKERS_UPDATE_INTERVAL = int(getattr(settings, 'DEFAULT_TRACKERS_UPDATE_INTERVAL', 10800) / 60)


@db_periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
def crawl_tracking_statuses():
    tracking.update_trackers()


@db_task()
def notify_webhooks(*args, **kwargs):
    webhook.notify_webhook_subscribers(*args, **kwargs)
