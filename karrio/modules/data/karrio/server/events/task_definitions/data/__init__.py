__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

import typing
import logging
from huey.contrib.djhuey import db_task

import karrio.server.core.utils as utils
import karrio.server.data.models as models
import karrio.server.data.serializers as serializers

logger = logging.getLogger(__name__)


@db_task()
@utils.error_wrapper
@utils.tenant_aware
def queue_batch_import(*args, **kwargs):
    from karrio.server.events.task_definitions.data import batch

    batch.trigger_batch_import(*args, **kwargs)


@db_task()
@utils.error_wrapper
@utils.tenant_aware
def save_batch_resources(*args, **kwargs):
    from karrio.server.events.task_definitions.data import batch

    batch.trigger_batch_saving(*args, **kwargs)


@db_task()
@utils.tenant_aware
def process_batch_resources(batch_id, **kwargs):
    logger.info(f"> start batch ({batch_id}) resources processing...")
    try:
        batch_operation = models.BatchOperation.objects.get(pk=batch_id)

        if batch_operation.resource_type == serializers.ResourceType.trackers.value:
            batch_operation.resources = _process_trackers(batch_operation.resources)

        elif batch_operation.resource_type == serializers.ResourceType.order.value:
            batch_operation.resources = _process_orders(batch_operation.resources)

        elif batch_operation.resource_type == serializers.ResourceType.shipment.value:
            batch_operation.resources = _process_shipments(batch_operation.resources)

        elif batch_operation.resource_type == serializers.ResourceType.billing.value:
            pass

        batch_operation.status = serializers.BatchOperationStatus.completed.value
        batch_operation.save(update_fields=["resources", "status"])
    except Exception as e:
        logger.exception(e)
        batch_operation.status = serializers.BatchOperationStatus.failed.value
        batch_operation.save()

    logger.info(f"> ending batch ({batch_id}) resources processing...")


def _process_shipments(resources: typing.List[dict]):
    from karrio.server.manager import models
    from karrio.server.events.task_definitions.data import shipments

    resource_ids = [res["id"] for res in resources]
    shipment_ids = [
        res["id"]
        for res in resources
        if res["status"] != serializers.ResourceStatus.processed.value
    ]
    shipments.process_shipments(shipment_ids=shipment_ids)
    # check results and update resource statuses
    results = models.Shipment.objects.filter(id__in=resource_ids)

    def _compute_state(shipment=None):
        # shipment with service not purchased
        if (
            any(shipment.options.get("perferred_service") or "")
            and shipment.status == "draft"
        ):
            return serializers.ResourceStatus.incomplete
        # shipment has errors and no rates
        if len(shipment.rates) == 0 and any(shipment.messages):
            return serializers.ResourceStatus.has_errors
        # shipment is at the right state
        return serializers.ResourceStatus.processed.value

    return [
        dict(
            id=res["id"],
            status=_compute_state(results.filter(id=res["id"]).first()),
        )
        for res in resources
    ]


def _process_orders(resources: typing.List[dict]):
    resource_ids = [res["id"] for res in resources]

    return [dict(id=id, status="processed") for id in resource_ids]


def _process_trackers(resources: typing.List[dict]):
    from karrio.server.manager import models
    from karrio.server.events.task_definitions.base import tracking

    resource_ids = [res["id"] for res in resources]
    tracker_ids = [
        res["id"]
        for res in resources
        if res["status"] != serializers.ResourceStatus.processed.value
    ]
    tracking.update_trackers(tracker_ids=tracker_ids)
    # check results and update resource statuses
    results = models.Tracking.objects.filter(id__in=resource_ids)

    def _compute_tracker_state(tracker=None):
        if tracker is None:
            return serializers.ResourceStatus.incomplete.value

        return serializers.ResourceStatus.processed.value

    return [
        dict(
            id=res["id"],
            status=_compute_tracker_state(results.filter(id=res["id"]).first()),
        )
        for res in resources
    ]


TASK_DEFINITIONS = [
    queue_batch_import,
    save_batch_resources,
    process_batch_resources,
]
