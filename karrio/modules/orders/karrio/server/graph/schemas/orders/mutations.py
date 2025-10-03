import typing
import strawberry
from strawberry.types import Info
import django.utils.timezone as timezone
import django.db.transaction as transaction

import karrio.lib as lib
import karrio.server.graph.utils as utils
import karrio.server.orders.models as models
import karrio.server.serializers as serializers
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.orders.types as types
import karrio.server.graph.schemas.orders.inputs as inputs
import karrio.server.orders.serializers.order as model_serializers


@strawberry.type
class CreateOrderMutation(utils.BaseMutation):
    order: typing.Optional[types.OrderType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["ORDERS_MANAGEMENT", "manage_orders"])
    def mutate(
        info: Info, **input: inputs.CreateOrderMutationInput
    ) -> "CreateOrderMutation":
        test_mode = info.context.request.test_mode
        order_id = "1" + str(
            models.Order.access_by(info.context.request).filter(source="draft").count()
            + 1
        ).zfill(
            5
        )  # TODO: make this grow beyond 2 million

        serializer = model_serializers.OrderSerializer(
            context=info.context.request,
            data={
                "order_id": order_id,
                "source": "draft",
                "test_mode": test_mode,
                "order_date": lib.fdate(timezone.now()),
                **lib.to_dict(input),
            },
        )
        serializer.is_valid(raise_exception=True)

        return CreateOrderMutation(order=serializer.save())  # type:ignore


@strawberry.type
class UpdateOrderMutation(utils.BaseMutation):
    order: typing.Optional[types.OrderType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    @utils.authorization_required(["ORDERS_MANAGEMENT", "manage_orders"])
    def mutate(
        info: Info,
        line_items: typing.Optional[
            typing.List[base.inputs.UpdateCommodityInput]
        ] = None,
        **input: inputs.UpdateOrderMutationInput,
    ) -> "UpdateOrderMutation":
        data = lib.to_dict(input)
        order = models.Order.access_by(info.context.request).get(
            id=input.get("id"),
            source="draft",
        )
        model_serializers.can_mutate_order(order, update=True, payload=data)

        serializer = model_serializers.OrderSerializer(
            order,
            context=info.context.request,
            data=data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        if any(line_items or ""):
            serializers.save_many_to_many_data(
                "line_items",
                model_serializers.LineItemModelSerializer,
                order,
                payload=dict(line_items=line_items),
                context=info.context.request,
            )

        serializer.save()

        # refetch the shipment to get the updated state with signals processed
        update = models.Order.access_by(info.context.request).get(id=input.get("id"))

        return UpdateOrderMutation(errors=None, order=update)  # type:ignore


@strawberry.type
class DeleteOrderMutation(utils.BaseMutation):
    id: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["ORDERS_MANAGEMENT", "manage_orders"])
    def mutate(
        info: Info, **input: inputs.DeleteOrderMutationInput
    ) -> "DeleteOrderMutation":
        id = input["id"]
        order = models.Order.access_by(info.context.request).get(id=id, source="draft")
        model_serializers.can_mutate_order(order, delete=True)

        order.delete()

        return DeleteOrderMutation(id=id)
