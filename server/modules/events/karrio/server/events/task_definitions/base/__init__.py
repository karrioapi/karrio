import logging
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task

import karrio.server.core.utils as utils

logger = logging.getLogger(__name__)
DEFAULT_TRACKERS_UPDATE_INTERVAL = int(
    getattr(settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200) / 60
)


@db_periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
def background_trackers_update():
    from karrio.server.events.task_definitions.base.tracking import update_trackers

    try:
        if settings.MULTI_TENANTS:
            import django_tenants.utils as tenant_utils

            for tenant in tenant_utils.get_tenant_model().objects.exclude(
                schema_name="public"
            ):
                with tenant_utils.tenant_context(tenant):
                    update_trackers()

        else:
            update_trackers()
    except Exception as e:
        logger.error(f"failed to crawl tracking statuses: {e}")


@db_task()
@utils.tenant_wrapper
def notify_webhooks(*args, **kwargs):
    from karrio.server.events.task_definitions.base.webhook import (
        notify_webhook_subscribers,
    )

    utils.failsafe(
        lambda: notify_webhook_subscribers(*args, **kwargs),
        "An error occured during webhook notification: $error",
    )


TASK_DEFINITIONS = [
    background_trackers_update,
    notify_webhooks,
]
