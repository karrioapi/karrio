import graphene
import graphene.types.generic as generic
from django.db.models import Q

import karrio.server.graph.utils as utils
import karrio.server.graph.extension.base.types as types
import karrio.server.manager.models as manager
import karrio.server.orders.models as models
import karrio.server.orders.serializers as serializers

OrderStatusEnum = graphene.Enum.from_enum(serializers.OrderStatus)


class LineItemType(types.CommodityType):
    unfulfilled_quantity = graphene.Int()

    class Meta:
        model = models.LineItem
        exclude = (
            *manager.Commodity.HIDDEN_PROPS,
            "commodity_order",
        )


class OrderType(utils.BaseObjectType):
    shipping_to = graphene.Field(graphene.NonNull(types.AddressType))
    shipping_from = graphene.Field(types.AddressType)
    billing_address = graphene.Field(types.AddressType)
    line_items = graphene.List(
        graphene.NonNull(LineItemType), required=True, default_value=[]
    )
    shipments = graphene.List(
        graphene.NonNull(types.ShipmentType), required=True, default_value=[]
    )

    metadata = generic.GenericScalar()
    options = generic.GenericScalar()

    status = OrderStatusEnum(required=True)

    class Meta:
        model = models.Order
        exclude = (*models.Order.HIDDEN_PROPS,)
        interfaces = (utils.CustomNode,)

    def resolve_line_items(self, info):
        return self.line_items.all()
