import tablib
import logging
from django.db import transaction

from karrio.server.conf import settings
import karrio.server.core.exceptions as exceptions
import karrio.server.data.models as models
import karrio.server.data.resources as resources
import karrio.server.data.serializers as serializers
import karrio.server.data.serializers.batch as batch

logger = logging.getLogger(__name__)


@serializers.owned_model_serializer
class DataTemplateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataTemplate
        exclude = ["created_at", "updated_at", "created_by", "org"]


@serializers.owned_model_serializer
class ImportDataSerializer(serializers.ImportData):
    @transaction.atomic
    def create(
        self, validated_data: dict, context: serializers.Context, **kwargs
    ) -> models.BatchOperation:
        import karrio.server.events.tasks as tasks

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
        resource = resources.get_import_resource(
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
            batch.BatchOperationModelSerializer.map(
                data=dict(resource_type=resource_type, test_mode=context.test_mode),
                context=context,
            )
            .save()
            .instance
        )

        tasks.queue_batch_import(
            operation.id,
            data=dict(
                dataset=dataset,
                import_data=validated_data,
            ),
            ctx=dict(
                org_id=getattr(context.org, "id", None),
                user_id=getattr(context.user, "id", None),
                test_mode=context.test_mode,
            ),
            schema=settings.schema,
        )

        return operation


def check_dataset_validation_errors(validation):
    if any(validation.base_errors):
        raise exceptions.APIExceptions(
            validation.base_errors,
            code="invalid_data",
        )

    errors = []
    flattened_row_errors = sum(
        [
            [(i, e.error) for e in row.errors]
            for i, row in enumerate(validation.rows)
        ],
        []
    )

    for index, error in flattened_row_errors:
        setattr(error, "index", index)
        errors.append(error)

    if any(errors):
        raise exceptions.APIExceptions(
            errors,
            code="invalid_data",
        )
