import graphene
import django_filters
import graphene.types.generic as generic
import graphene_django
from django.db.models import Q

from purplship.server.graph.extension.base.types import *
import purplship.server.orders.models as models
import purplship.server.orders.serializers as serializers

OrderStatusEnum = graphene.Enum.from_enum(serializers.OrderStatus)


class OrderFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(
        field_name="shipping_address__address_line1", lookup_expr="icontains"
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
    option_key = CharInFilter(
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

    def option_key_filter(self, queryset, name, value):
        return queryset.filter(Q(options__has_key=value))

    def option_value_filter(self, queryset, name, value):
        return queryset.filter(Q(options__values__contains=value))

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__values__contains=value))


class OrderType(graphene_django.DjangoObjectType):
    shipping_address = graphene.Field(AddressType)
    line_items = graphene.List(CommodityType)
    shipments = graphene.List(ShipmentType)

    metadata = generic.GenericScalar()
    options = generic.GenericScalar()

    status = OrderStatusEnum(required=True)

    class Meta:
        model = models.Order
        exclude = ("org",)
        interfaces = (CustomNode,)

    def resolve_line_items(self, info):
        return self.line_items.all()
