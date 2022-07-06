import typing
import logging
import tablib
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
from import_export.resources import ModelResource

import karrio.server.manager.models as manager
import karrio.server.data.serializers as serializers
import karrio.server.data.resources as resources
import karrio.server.data.models as models

logger = logging.getLogger(__name__)
User = get_user_model()


def trigger_batch_processing(
    batch_id: str,
    data: dict,
    ctx: dict,
    test_mode: bool = None,
    **kwargs,
):
    logger.info(f"> starting batch operation processing ({batch_id})")
    try:
        context = retrieve_context(ctx)
        batch_operation = (
            models.BatchOperation.access_by(context).filter(pk=batch_id).first()
        )

        if batch_operation is not None:
            import_data = data["import_data"]
            dataset = data["dataset"]
            resource = resources.get_resource(
                resource_type=batch_operation.resource_type,
                params=import_data,
                context=context,
            )

            batch_resources = process_resources(
                batch_operation.resource_type, resource, dataset, context
            )
            update_batch_operation_resources(batch_operation, batch_resources)
        else:
            logger.info("batch operation not found")

    except Exception as e:
        logger.error(e)

    logger.info(f"> ending batch operation processing ({batch_id})")


def process_resources(
    resource_type: str,
    resource: ModelResource,
    dataset: tablib.Dataset,
    context: serializers.Context,
):
    result = resource.import_data(dataset, dry_run=False)

    _object_model = serializers.ResourceType.get_model(resource_type)
    _object_ids = [row.object_id for row in result.rows]
    _objects: list = []
    for _object in _object_model.objects.filter(id__in=_object_ids):
        _object.link = _object.__class__.link.related.related_model.objects.create(
            org=context.org, item=_object
        )

    _object_model.objects.bulk_update(_objects, fields=["updated_at"])

    return [
        dict(id=id, status=serializers.ResourceStatus.queued.value)
        for id in _object_ids
    ]


def update_batch_operation_resources(
    batch_operation: models.BatchOperation,
    batch_resources: typing.List[dict],
):
    try:
        logger.debug(f"update batch operation {batch_operation.id}")

        batch_operation.status = serializers.BatchOperationStatus.running.value
        batch_operation.resources = batch_resources
        batch_operation.save(update_fields=["resources", "status"])

        logger.debug(f"batch operation {batch_operation.id} updated successfully")
    except Exception as update_error:
        logger.warning(f"failed to update batch operation {batch_operation.id}")
        logger.error(update_error, exc_info=True)


def retrieve_context(info: dict) -> serializers.Context:
    org = None

    if settings.MULTI_ORGANIZATIONS and "org_id" in info:
        import karrio.server.orgs.models as orgs_models

        org = orgs_models.Organization.objects.filter(id=info["org_id"]).first()

    return serializers.Context(
        org=org,
        user=User.objects.filter(id=info["user_id"]).first(),
    )
