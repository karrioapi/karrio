import tablib
import logging
from django.db import transaction

from karrio.server.conf import settings
import karrio.server.events.tasks as tasks
import karrio.server.core.exceptions as exceptions
import karrio.server.data.models as models
import karrio.server.data.resources as resources
import karrio.server.data.serializers as serializers
import karrio.server.data.serializers.batch as batch

logger = logging.getLogger(__name__)


@serializers.owned_model_serializer
class ImportDataSerializer(serializers.ImportData):
    @transaction.atomic
    def create(
        self, validated_data: dict, context: serializers.Context, **kwargs
    ) -> models.BatchOperation:
        test_mode = getattr(context, "test_mode", False)
        resource_type = validated_data["resource_type"]
        data_field = validated_data["data_file"]
        template = (
            models.DataTemplate.access_by(context).first(
                slug=validated_data.get("data_template")
            )
            if "data_template" in validated_data
            else None
        )
        data_fields: dict = getattr(
            template,
            "data_fields",
            serializers.ResourceType.get_default_mapping(resource_type),
        )
        resource = resources.get_resource(
            resource_type=resource_type,
            data_fields=data_fields,
            params=validated_data,
            context=context,
        )
        dataset = tablib.Dataset().load(
            data_field.read().decode(),
            headers=data_fields.values(),
        )

        # dry run data import to validate file content.
        validation = resource.import_data(dataset, dry_run=True)
        check_dataset_validation_errors(validation)

        operation = (
            serializers.SerializerDecorator[batch.BatchOperationModelSerializer](
                data=dict(resource_type=resource_type, test_mode=test_mode),
                context=context,
            )
            .save()
            .instance
        )

        tasks.queue_batch(
            operation.id,
            schema=settings.schema,
            data=dict(
                dataset=dataset,
                import_data=validated_data,
            ),
            ctx=dict(
                org_id=getattr(context.org, "id", None),
                user_id=getattr(context.user, "id", None),
            ),
        )

        return operation


def check_dataset_validation_errors(validation):

    errors = [
        err.error
        for err in sum([row.errors for row in validation.rows], validation.base_errors)
    ]

    if any(errors):
        raise exceptions.APIExceptions(
            errors,
            code="invalid_data",
        )
