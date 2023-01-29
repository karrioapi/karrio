__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

import time
import logging
from django.conf import settings
from huey.contrib.djhuey import db_task

import karrio.server.core.utils as utils
import karrio.server.orgs.models as models

logger = logging.getLogger(__name__)


@db_task()
@utils.error_wrapper
@utils.async_wrapper
@utils.tenant_aware
def cleanup_orgs(**kwargs):
    if settings.MULTI_TENANTS and kwargs.get("schema") == "public":
        return

    time.sleep(5)
    logger.info(f"> cleanup organizations...")
    models.Organization.objects.filter(owner__isnull=True, users__isnull=True).delete()


TASK_DEFINITIONS = [
    cleanup_orgs,
]
