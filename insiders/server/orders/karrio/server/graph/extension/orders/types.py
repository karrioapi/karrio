import graphene
import django_filters
import graphene.types.generic as generic
from django.db.models import Q

import karrio.server.graph.utils as utils
import karrio.server.graph.extension.base.types as types
import karrio.server.manager.models as manager
import karrio.server.orders.models as models
import karrio.server.orders.serializers as serializers

OrderStatusEnum = graphene.Enum.from_enum(serializers.OrderStatus)


class OrderFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(
        field_name="shipping_to__address_line1", lookup_expr="icontains"
    )
    id = utils.CharInFilter(
        field_name="id",
        method="id_filter",
    )
    order_id = utils.CharInFilter(
        field_name="order_id",
        method="order_id_filter",
    )
    source = utils.CharInFilter(
        field_name="source",
        method="channel_filter",
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    status = django_filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.OrderStatus)],
    )
    option_key = utils.CharInFilter(
        field_name="options",
        method="option_key_filter",
    )
    option_value = django_filters.CharFilter(
        field_name="options",
        method="option_value_filter",
    )
    metadata_value = django_filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
    )
    test_mode = django_filters.BooleanFilter(field_name="test_mode")

    class Meta:
        model = models.Order
        fields: list = []

    def id_filter(self, queryset, name, value):
        return queryset.filter(Q(id__in=value))

    def order_id_filter(self, queryset, name, value):
        return queryset.filter(Q(order_id__in=value))

    def source_filter(self, queryset, name, value):
        return queryset.filter(Q(source__in=value))

    def option_key_filter(self, queryset, name, value):
        return queryset.filter(Q(options__has_key=value))

    def option_value_filter(self, queryset, name, value):
        return queryset.filter(Q(options__values__contains=value))

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__values__contains=value))


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
