__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

import logging
from huey.contrib.djhuey import db_task

import karrio.server.core.utils as utils

logger = logging.getLogger(__name__)


@db_task()
@utils.error_wrapper
@utils.tenant_aware
def queue_workflow_event(*args, **kwargs):
    import karrio.server.events.task_definitions.automation.workflow as workflow

    workflow.run_workflow(*args, **kwargs)


TASK_DEFINITIONS = [
    queue_workflow_event,
]
