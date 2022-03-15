import logging
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task

logger = logging.getLogger(__name__)
DEFAULT_TRACKERS_UPDATE_INTERVAL = int(
    getattr(settings, "DEFAULT_TRACKERS_UPDATE_INTERVAL", 7200) / 60
)


@db_periodic_task(crontab(minute=f"*/{DEFAULT_TRACKERS_UPDATE_INTERVAL}"))
def crawl_tracking_statuses():
    from karrio.server.events.tasks.tracking import update_trackers

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
def notify_webhooks(*args, **kwargs):
    from karrio.server.events.tasks.webhook import notify_webhook_subscribers

    try:
        if settings.MULTI_TENANTS:
            import django_tenants.utils as tenant_utils

            with tenant_utils.schema_context(kwargs.get("schema")):
                notify_webhook_subscribers(*args, **kwargs)

        else:
            notify_webhook_subscribers(*args, **kwargs)
    except Exception as e:
        logger.error(f"failed to notify webhooks: {e}")
