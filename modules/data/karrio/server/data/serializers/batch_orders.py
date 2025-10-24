from django.db import transaction

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.orders.models as orders
import karrio.server.serializers as serializers
import karrio.server.data.serializers.base as base
import karrio.server.core.exceptions as exceptions
import karrio.server.orders.serializers as order_serializers


@serializers.owned_model_serializer
class BatchOrderData(serializers.Serializer):
    orders = order_serializers.OrderData(
        many=True,
        allow_empty=False,
        help_text="The list of orders to process.",
    )

    @transaction.atomic
    def create(self, validated_data: dict, context: serializers.Context, **kwargs):
        import karrio.server.events.tasks as tasks
        import karrio.server.data.serializers.batch as batch

        operation_data = dict(resource_type="orders", test_mode=context.test_mode)
        operation = (
            batch.BatchOperationModelSerializer.map(
                data=operation_data, context=context
            )
            .save()
            .instance
        )

        sid = transaction.savepoint()
        resources = BatchOrderData.save_resources(
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
        orders_data = data["orders"]
        resources = []

        for index, order_data in enumerate(orders_data):
            try:
                queryset = orders.Order.access_by(context).filter(
                    order_id=order_data["order_id"], source=order_data["source"]
                )
                order = (
                    queryset.first()
                    if queryset.exists()
                    else (
                        order_serializers.OrderSerializer.map(
                            data=order_data, context=context
                        )
                        .save()
                        .instance
                    )
                )
                resources.append(
                    dict(id=order.id, status=base.ResourceStatus.queued.value)
                )
            except Exception as e:
                setattr(e, "index", index)
                resources.append(
                    dict(
                        id=index,
                        status=base.ResourceStatus.has_errors.value,
                        errors=(lib.to_dict(e) if format_errors else e),
                    )
                )

        return resources
