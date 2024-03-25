from django.db import transaction

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.manager.models as manager
import karrio.server.serializers as serializers
import karrio.server.core.exceptions as exceptions
import karrio.server.data.serializers.base as base
import karrio.server.manager.serializers as manager_serializers


class ShipmentDataReference(manager_serializers.ShipmentData):
    id = serializers.CharField(
        help_text="The shipment id.",
        required=False,
    )


@serializers.owned_model_serializer
class BatchShipmentData(serializers.Serializer):
    shipments = ShipmentDataReference(
        many=True,
        allow_empty=False,
        help_text="The list of shipments to process.",
    )

    @transaction.atomic
    def create(self, validated_data: dict, context: serializers.Context, **kwargs):
        import karrio.server.events.tasks as tasks
        import karrio.server.data.serializers.batch as batch

        operation_data = dict(resource_type="shipments", test_mode=context.test_mode)
        operation = (
            batch.BatchOperationModelSerializer.map(
                data=operation_data, context=context
            )
            .save()
            .instance
        )

        sid = transaction.savepoint()
        resources = BatchShipmentData.save_resources(
            context=context,
            data=validated_data,
            batch_id=operation.id,
            format_errors=False,
        )
        errors = [r["errors"] for r in resources if r.get("errors") is not None]
        transaction.savepoint_rollback(sid)

        if any(errors):
            raise exceptions.APIExceptions(errors, code="invalid_data")

        tasks.save_batch_resources(
            operation.id,
            data=validated_data,
            schema=conf.settings.schema,
            ctx=dict(
                test_mode=context.test_mode,
                org_id=getattr(context.org, "id", None),
                user_id=getattr(context.user, "id", None),
            ),
        )

        return operation

    @staticmethod
    def save_resources(
        data: dict,
        batch_id: str,
        context: serializers.Context,
        format_errors: bool = True,
    ):
        shipments_data = data["shipments"]
        resources = []

        for index, shipment_data in enumerate(shipments_data):
            try:
                shipment = (
                    manager.Shipment.access_by(context).get(id=shipment_data["id"])
                    if shipment_data.get("id") is not None
                    else (
                        manager_serializers.ShipmentSerializer.map(
                            data=shipment_data, context=context
                        )
                        .save(fetch_rates=False)
                        .instance
                    )
                )
                resources.append(
                    dict(id=shipment.id, status=base.ResourceStatus.queued.value)
                )
            except Exception as e:
                resources.append(
                    dict(
                        id=index,
                        status=base.ResourceStatus.has_errors.value,
                        errors=(lib.to_dict(e) if format_errors else e),
                    )
                )

        return resources
