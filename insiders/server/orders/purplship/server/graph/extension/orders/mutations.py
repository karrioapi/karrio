import graphene
from graphene.types import generic

from purplship.core.utils import DP

import purplship.server.orders.models as models
import purplship.server.orders.serializers as serializers
import purplship.server.graph.extension.orders.types as types
import purplship.server.graph.extension.base.inputs as inputs
import purplship.server.graph.extension.base.mutations as mutations
from purplship.server.orders.serializers.order import (
    OrderSerializer,
    can_mutate_order,
)


class PartialOrderUpdate(mutations.ClientMutation):
    order = graphene.Field(types.OrderType)

    class Input:
        id = graphene.String(required=True)
        shipping_address = graphene.Field(inputs.UpdateAddressInput, required=False)
        line_items = graphene.List(inputs.UpdateCommodityInput, required=False)
        options = generic.GenericScalar(required=False)
        metadata = generic.GenericScalar(required=False)

    @classmethod
    @types.login_required
    def mutate_and_get_payload(cls, root, info, id: str, **inputs):
        order = models.Order.access_by(info.context).get(id=id)
        can_mutate_order(order, update=True)

        serializers.SerializerDecorator[OrderSerializer](
            order,
            context=info.context,
            data=DP.to_dict(inputs),
        ).save()

        return cls(errors=None, order=order)
