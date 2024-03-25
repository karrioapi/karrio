import typing
import tablib
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from import_export.resources import ModelResource

import karrio.server.core.utils as utils
import karrio.server.data.serializers as serializers
import karrio.server.data.resources as resources
import karrio.server.data.models as models

logger = logging.getLogger(__name__)
User = get_user_model()


@utils.tenant_aware
def trigger_batch_import(
    batch_id: str,
    data: dict,
    ctx: dict,
    **kwargs,
):
    logger.info(f"> starting batch import operation ({batch_id})")
    try:
        context = retrieve_context(ctx)
        batch_operation = (
            models.BatchOperation.access_by(context).filter(pk=batch_id).first()
        )

        if batch_operation is not None:
            dataset = data["dataset"]
            import_data = data["import_data"]
            resource = resources.get_import_resource(
                resource_type=batch_operation.resource_type,
                params=import_data,
                context=context,
                batch_id=batch_id,
            )

            batch_resources = process_resources(resource, dataset)
            update_batch_operation_resources(batch_operation, batch_resources)
        else:
            logger.info("batch operation not found")

    except Exception as e:
        logger.exception(e)

    logger.info(f"> ending batch import operation ({batch_id})")


@utils.tenant_aware
def trigger_batch_saving(
    batch_id: str,
    data: dict,
    ctx: dict,
    **kwargs,
):
    logger.info(f"> beging batch resources saving ({batch_id})")
    try:
        context = retrieve_context(ctx)
        batch_operation = (
            models.BatchOperation.access_by(context).filter(pk=batch_id).first()
        )

        if batch_operation is not None:
            batch_seriazlizer = serializers.ResourceType.get_serialiazer(
                batch_operation.resource_type
            )
            batch_resources = batch_seriazlizer.save_resources(data, batch_id, context)
            update_batch_operation_resources(batch_operation, batch_resources)
        else:
            logger.info("batch operation not found")

    except Exception as e:
        logger.exception(e)

    logger.info(f"> ending batch resources saving ({batch_id})")


def process_resources(
    resource: ModelResource,
    dataset: tablib.Dataset,
):
    result = resource.import_data(dataset, dry_run=False)
    _object_ids = [(row.object_id, row.errors) for row in result.rows]

    return [
        dict(
            id=id,
            status=(
                serializers.ResourceStatus.failed.value
                if any(errors)
                else serializers.ResourceStatus.queued.value
            ),
        )
        for id, errors in _object_ids
    ]


def update_batch_operation_resources(
    batch_operation: models.BatchOperation,
    batch_resources: typing.List[dict],
):
    try:
        logger.debug(f"update batch operation {batch_operation.id}")

        batch_operation.resources = batch_resources
        batch_operation.status = serializers.BatchOperationStatus.running.value
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
        test_mode=(info.get("test_mode") or False),
    )
