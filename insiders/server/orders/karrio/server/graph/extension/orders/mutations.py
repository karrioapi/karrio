import datetime
import graphene
from graphene.types import generic
from graphene_django.types import ErrorType

from karrio.core.utils import DP
import karrio.server.graph.utils as utils
import karrio.server.orders.models as models
import karrio.server.graph.extension.orders.types as types
import karrio.server.graph.extension.base.inputs as inputs
from karrio.server.orders.serializers.order import (
    OrderSerializer,
    can_mutate_order,
)


class CreateOrder(utils.ClientMutation):
    order = graphene.Field(types.OrderType)

    class Input:
        order_id = graphene.String(required=False)
        order_date = graphene.Date(required=False)
        source = graphene.String(required=False, default_value="manual")
        shipping_to = graphene.Field(inputs.CreateAddressInput, required=True)
        shipping_from = graphene.Field(inputs.CreateAddressInput, required=False)
        line_items = graphene.List(inputs.CreateCommodityInput, required=True)
        options = generic.GenericScalar(required=False)
        metadata = generic.GenericScalar(required=False)
        test_mode = graphene.Boolean(required=False, default_value=False)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, **inputs):
        serializer = OrderSerializer(
            context=info.context,
            data=DP.to_dict(inputs),
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        serializer.save()

        order = models.Order.access_by(info.context).get(id=id)

        return cls(errors=None, order=order)


class PartialOrderUpdate(utils.ClientMutation):
    order = graphene.Field(types.OrderType)

    class Input:
        id = graphene.String(required=True)
        order_id = graphene.String(required=False)
        order_date = graphene.Date(required=False)
        source = graphene.String(required=False)
        shipping_to = graphene.Field(inputs.UpdateAddressInput, required=False)
        shipping_from = graphene.Field(inputs.UpdateAddressInput, required=False)
        line_items = graphene.List(inputs.UpdateCommodityInput, required=False)
        options = generic.GenericScalar(required=False)
        metadata = generic.GenericScalar(required=False)
        test_mode = graphene.Boolean(required=False)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, id: str, **inputs):
        order = models.Order.access_by(info.context).get(id=id)
        can_mutate_order(order, update=True)

        serializer = OrderSerializer(
            order,
            context=info.context,
            data=DP.to_dict(inputs),
            partial=True,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        serializer.save()

        # refetch the shipment to get the updated state with signals processed
        update = models.Order.access_by(info.context).get(id=id)

        return cls(errors=None, order=update)
