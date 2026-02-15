"""
Background task definitions for the Karrio event system.

This module registers Huey tasks that the worker process consumes:

    Periodic tasks (cron-scheduled):
        background_trackers_update  — dispatches per-carrier tracking sub-tasks
        periodic_data_archiving     — archives stale data
        daily_pickup_close          — auto-closes past pickups

    On-demand tasks (enqueued by signals or the dispatcher):
        process_carrier_tracking_batch — fetches + saves tracking for one carrier
        notify_webhooks               — delivers webhook notifications

The dispatcher pattern (`background_trackers_update` → `process_carrier_tracking_batch`)
ensures O(n) wall-clock for tracking updates regardless of carrier count.  A Huey
task lock prevents duplicate dispatcher runs when overdue periodic tasks queue up
at worker startup.
"""

import logging
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task, HUEY as huey_instance
from huey.exceptions import TaskLockedException

import karrio.server.core.utils as utils
from karrio.server.core.telemetry import with_task_telemetry

logger = logging.getLogger(__name__)

DATA_ARCHIVING_SCHEDULE = int(getattr(settings, "DATA_ARCHIVING_SCHEDULE", 168))
DEFAULT_TRACKERS_UPDATE_INTERVAL = max(
    1,
    min(
        59,
        int(getattr(settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200) / 60),
    ),
)


# ─────────────────────────────────────────────────────────────────
# Tracking
# ─────────────────────────────────────────────────────────────────


@db_periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
@with_task_telemetry("background_trackers_update")
def background_trackers_update():
    from karrio.server.events.task_definitions.base import tracking

    try:
        with huey_instance.lock_task("background_trackers_update"):
            @utils.run_on_all_tenants
            def _run(**kwargs):
                tracking.update_trackers(schema=kwargs.get("schema"))

            _run()
    except TaskLockedException:
        logger.info("Tracker update already in progress, skipping duplicate run")


@db_task(retries=2, retry_delay=30)
@utils.tenant_aware
@with_task_telemetry("process_carrier_tracking_batch")
def process_carrier_tracking_batch(*args, **kwargs):
    from karrio.server.events.task_definitions.base import tracking

    tracking.process_carrier_trackers(*args, **kwargs)


# ─────────────────────────────────────────────────────────────────
# Webhooks
# ─────────────────────────────────────────────────────────────────


@db_task(retries=5, retry_delay=60)
@utils.tenant_aware
@with_task_telemetry("notify_webhooks")
def notify_webhooks(*args, **kwargs):
    from karrio.server.events.task_definitions.base import webhook

    webhook.notify_webhook_subscribers(*args, **kwargs)


# ─────────────────────────────────────────────────────────────────
# Maintenance
# ─────────────────────────────────────────────────────────────────


@db_periodic_task(crontab(minute=0, hour=0))
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


@db_periodic_task(crontab(hour=0, minute=30))
@with_task_telemetry("daily_pickup_close")
def daily_pickup_close():
    from karrio.server.events.task_definitions.base import pickup

    @utils.run_on_all_tenants
    def _run(**kwargs):
        utils.failsafe(
            lambda: pickup.close_past_pickups(),
            "An error occurred during pickup auto-close: $error",
        )

    _run()


# ─────────────────────────────────────────────────────────────────
# Registry (consumed by the Huey worker for task discovery)
# ─────────────────────────────────────────────────────────────────

TASK_DEFINITIONS = [
    background_trackers_update,
    process_carrier_tracking_batch,
    periodic_data_archiving,
    daily_pickup_close,
    notify_webhooks,
]
