from django.db import transaction

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.serializers as serializers
import karrio.server.core.exceptions as exceptions
import karrio.server.manager.serializers as manager
import karrio.server.data.serializers.base as base


@serializers.owned_model_serializer
class BatchShipmentData(serializers.Serializer):
    shipments = manager.ShipmentData(
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
            batch.BatchOperationModelSerializer
            .map(data=operation_data, context=context)
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
        errors = [r['errors'] for r in resources if r.get('errors') is not None]
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
    def save_resources(data: dict, batch_id: str, context: serializers.Context, format_errors: bool = True):
        from karrio.server.manager.serializers import ShipmentSerializer

        meta = dict(batch_id=batch_id)
        shipments_data = data['shipments']
        resources = []

        for index, shipment_data in enumerate(shipments_data):
            try:
                shipment = (
                    ShipmentSerializer
                    .map(data={**shipment_data, "meta": meta}, context=context)
                    .save(fetch_rates=False)
                    .instance
                )
                resources.append(dict(
                    id=shipment.id,
                    status=base.ResourceStatus.queued.value
                ))
            except Exception as e:
                resources.append(dict(
                    id=index,
                    status=base.ResourceStatus.has_errors.value,
                    errors=(lib.to_dict(e) if format_errors else e),
                ))

        return resources
