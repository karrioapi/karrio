__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

import logging
from django.conf import settings
from huey.contrib.djhuey import db_task

logger = logging.getLogger(__name__)


@db_task()
def queue_batch(*args, **kwargs):
    from karrio.server.events.tasks_definitions.data.batch import (
        trigger_batch_processing,
    )

    try:
        if settings.MULTI_TENANTS:
            import django_tenants.utils as tenant_utils

            with tenant_utils.schema_context(kwargs.get("schema")):
                trigger_batch_processing(*args, **kwargs)

        else:
            trigger_batch_processing(*args, **kwargs)
    except:
        logger.error("batch processing failed")


TASK_DEFINITIONS = [
    queue_batch,
]
