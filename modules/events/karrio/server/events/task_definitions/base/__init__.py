import time
import logging
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task

import karrio.server.core.utils as utils

logger = logging.getLogger(__name__)
DATA_ARCHIVING_SCHEDULE = int(getattr(settings, "DATA_ARCHIVING_SCHEDULE", 168))
DEFAULT_TRACKERS_UPDATE_INTERVAL = int(
    getattr(settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200) / 60
)


@db_periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
def background_trackers_update():
    from karrio.server.events.task_definitions.base import tracking

    @utils.run_on_all_tenants
    def _run(**kwargs):
        try:
            tracking.update_trackers()
        except Exception as e:
            logger.error(f"An error occured during tracking statuses update: {e}")

    _run()


@db_task()
@utils.tenant_aware
def notify_webhooks(*args, **kwargs):
    from karrio.server.events.task_definitions.base import webhook

    utils.failsafe(
        lambda: webhook.notify_webhook_subscribers(*args, **kwargs),
        "An error occured during webhook notification: $error",
    )


@db_periodic_task(crontab(hour=f"*/{DATA_ARCHIVING_SCHEDULE}"))
def periodic_data_archiving(*args, **kwargs):
    from karrio.server.events.task_definitions.base import archiving

    @utils.run_on_all_tenants
    def _run(**kwargs):
        try:
            utils.failsafe(
                lambda: archiving.run_data_archiving(*args, **kwargs),
                "An error occured during data archiving: $error",
            )
        except Exception as e:
            logger.error(f"An error occured during data archiving: {e}")

    _run()

TASK_DEFINITIONS = [
    background_trackers_update,
    periodic_data_archiving,
    notify_webhooks,
]
