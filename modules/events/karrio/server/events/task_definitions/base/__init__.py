import logging
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task

import karrio.server.core.utils as utils
from karrio.server.core.telemetry import with_task_telemetry

logger = logging.getLogger(__name__)
DATA_ARCHIVING_SCHEDULE = int(getattr(settings, "DATA_ARCHIVING_SCHEDULE", 168))
DEFAULT_TRACKERS_UPDATE_INTERVAL = int(
    getattr(settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200) / 60
)


@db_periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
@with_task_telemetry("background_trackers_update")
def background_trackers_update():
    from karrio.server.events.task_definitions.base import tracking

    @utils.run_on_all_tenants
    def _run(**kwargs):
        tracking.update_trackers()

    _run()


@db_task(retries=5, retry_delay=60)
@utils.tenant_aware
@with_task_telemetry("notify_webhooks")
def notify_webhooks(*args, **kwargs):
    from karrio.server.events.task_definitions.base import webhook

    webhook.notify_webhook_subscribers(*args, **kwargs)


@db_periodic_task(crontab(hour=f"*/{DATA_ARCHIVING_SCHEDULE}"))
@with_task_telemetry("periodic_data_archiving")
def periodic_data_archiving(*args, **kwargs):
    from karrio.server.events.task_definitions.base import archiving

    @utils.run_on_all_tenants
    def _run(**kwargs):
        utils.failsafe(
            lambda: archiving.run_data_archiving(*args, **kwargs),
            "An error occured during data archiving: $error",
        )

    _run()


TASK_DEFINITIONS = [
    background_trackers_update,
    periodic_data_archiving,
    notify_webhooks,
]
