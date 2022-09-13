__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

import logging
from django.conf import settings
from huey.contrib.djhuey import db_task

import karrio.server.core.utils as utils
import karrio.server.data.models as models
import karrio.server.data.serializers as serializers

logger = logging.getLogger(__name__)


@db_task()
@utils.tenant_aware
def queue_batch(*args, **kwargs):
    try:
        from karrio.server.events.task_definitions.data.batch import (
            trigger_batch_processing,
        )

        if settings.MULTI_TENANTS:
            import django_tenants.utils as tenant_utils

            with tenant_utils.schema_context(kwargs.get("schema")):
                trigger_batch_processing(*args, **kwargs)
        else:
            trigger_batch_processing(*args, **kwargs)
    except:
        logger.error("batch processing failed")


@db_task()
@utils.tenant_aware
def process_batch_resources(batch_id, **kwargs):
    logger.info(f"> start batch ({batch_id}) resources processing...")
    try:
        batch_operation = models.BatchOperation.objects.get(pk=batch_id)

        if batch_operation.resource_type == serializers.ResourceType.tracking.value:
            from karrio.server.events.task_definitions.base import tracking

            tracker_ids = [res["id"] for res in batch_operation.resources]
            tracking.update_trackers(tracker_ids=tracker_ids)
            # check results and update resource statuses
            trackers = serializers.ResourceType.get_model(
                batch_operation.resource_type
            ).objects.filter(id__in=tracker_ids)
            batch_operation.resources = [
                dict(
                    id=id, status=_compute_tracker_state(trackers.filter(id=id).first())
                )
                for id in tracker_ids
            ]
            batch_operation.status = serializers.BatchOperationStatus.completed.value
            batch_operation.save(update_fields=["resources", "status"])

        elif batch_operation.resource_type == serializers.ResourceType.order.value:
            pass

        elif batch_operation.resource_type == serializers.ResourceType.shipment.value:
            pass

        elif batch_operation.resource_type == serializers.ResourceType.billing.value:
            pass

    except Exception as e:
        logger.error(e)
        batch_operation.status = serializers.BatchOperationStatus.failed.value
        batch_operation.save()

    logger.info(f"> ending batch ({batch_id}) resources processing...")


def _compute_tracker_state(tracker=None) -> serializers.ResourceStatus:
    if tracker is None:
        return serializers.ResourceStatus.failed.value

    return serializers.ResourceStatus.processed.value


TASK_DEFINITIONS = [
    queue_batch,
    process_batch_resources,
]
