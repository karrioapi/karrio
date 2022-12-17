import typing
import strawberry
from strawberry.types import Info

import karrio.lib as lib
import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.orders.types as types
import karrio.server.graph.schemas.orders.inputs as inputs
import karrio.server.orders.serializers.order as serializers
import karrio.server.orders.models as models


@strawberry.type
class CreateOrderMutation(utils.BaseMutation):
    order: typing.Optional[types.OrderType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["ORDERS_MANAGEMENT", "manage_orders"])
    def mutate(
        info: Info, **input: inputs.CreateOrderMutationInput
    ) -> "CreateOrderMutation":
        count = (
            models.Order.access_by(info.context.request).filter(source="manual").count()
            + 1
        )
        order_id = "1" + str(count).zfill(5)  # TODO: make this grow beyond 2 million

        serializer = serializers.OrderSerializer(
            context=info.context,
            data={
                **lib.to_dict(input),
                "source": "manual",
                "order_id": order_id,
            },
        )
        serializer.is_valid(raise_exception=True)

        return CreateOrderMutation(order=serializer.save())  # type:ignore


@strawberry.type
class PartialOrderUpdateMutation(utils.BaseMutation):
    order: typing.Optional[types.OrderType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["ORDERS_MANAGEMENT", "manage_orders"])
    def mutate(
        info: Info, **input: inputs.PartialOrderUpdateMutationInput
    ) -> "PartialOrderUpdateMutation":
        data = lib.to_dict(input)
        order = models.Order.access_by(info.context.request).get(id=input.get("id"))
        serializers.can_mutate_order(order, update=True, payload=data)

        serializer = serializers.OrderSerializer(
            order,
            context=info.context,
            data=data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # refetch the shipment to get the updated state with signals processed
        update = models.Order.access_by(info.context.request).get(id=input.get("id"))

        return PartialOrderUpdateMutation(errors=None, order=update)  # type:ignore
