__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

import logging
import time
from huey.contrib.djhuey import db_task

import karrio.server.core.utils as utils
import karrio.server.orgs.models as models

logger = logging.getLogger(__name__)


@db_task()
@utils.tenant_wrapper
def cleanup_orgs(*args, **kwargs):
    @utils.run_async
    def _actual():
        try:
            time.sleep(5)
            logger.info(f"> cleanup organizations...")
            models.Organization.objects.filter(
                owner__isnull=True, users__isnull=True
            ).delete()
        except Exception as e:
            logger.warning(f"Error during organizations cleanup {e}")

    _actual()


TASK_DEFINITIONS = [
    cleanup_orgs,
]
