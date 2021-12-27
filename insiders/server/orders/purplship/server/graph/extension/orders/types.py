import graphene
import django_filters
import graphene.types.generic as generic
import graphene_django
from django.db.models import Q

import purplship.server.orders.serializers as serializers
import purplship.server.graph.extension.base.types as basetypes
import purplship.server.orders.models as models


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
    option_key = basetypes.CharInFilter(
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
        fields = []

    def option_key_filter(self, queryset, name, value):
        return queryset.filter(Q(options__has_key=value))

    def option_value_filter(self, queryset, name, value):
        return queryset.filter(Q(options__values__contains=value))

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__values__contains=value))


class OrderType(graphene_django.DjangoObjectType):
    shipping_address = graphene.Field(basetypes.AddressType, required=True)
    line_items = graphene.List(basetypes.CommodityType, required=True)
    shipments = graphene.List(basetypes.ShipmentType, required=True)

    metadata = generic.GenericScalar()
    options = generic.GenericScalar()
    meta = generic.GenericScalar()

    status = graphene.Enum.from_enum(serializers.OrderStatus)(required=True)

    class Meta:
        model = models.Order
        exclude = ("org",)
        interfaces = (basetypes.CustomNode,)

    def resolve_line_items(self, info):
        return self.line_items.all()

    def resolve_shipments(self, info):
        return self.shipments.all()
