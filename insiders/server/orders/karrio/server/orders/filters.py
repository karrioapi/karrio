from django_filters import rest_framework as filters
from django.db.models import Q

from karrio.server.core.filters import CharInFilter
from karrio.server.orders import serializers
import karrio.server.orders.models as models


class OrderFilters(filters.FilterSet):
    address = filters.CharFilter(
        field_name="shipping_to__address_line1",
        lookup_expr="icontains",
        help_text="customer address line",
    )
    id = CharInFilter(
        field_name="id",
        method="id_filter",
        help_text="id(s). multiple separated by comma",
    )
    order_id = CharInFilter(
        field_name="order_id",
        method="order_id_filter",
        help_text="source order order_id(s). multiple separated by comma",
    )
    source = CharInFilter(
        field_name="source",
        method="channel_filter",
        help_text="order source(s). multiple separated by comma",
    )
    created_after = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        help_text="DateTime in format `YYYY-MM-DD H:M:S.fz`",
    )
    created_before = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        help_text="DateTime in format `YYYY-MM-DD H:M:S.fz`",
    )
    status = filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.OrderStatus)],
        help_text="order statuses. multiple separated by comma",
    )
    option_key = CharInFilter(
        field_name="options",
        method="option_key_filter",
        help_text="order option keys. multiple separated by comma",
    )
    option_value = filters.CharFilter(
        field_name="options",
        method="option_value_filter",
        help_text="order option value",
    )
    metadata_key = CharInFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="order metadata keys. multiple separated by comma",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="order metadata value",
    )
    test_mode = filters.BooleanFilter(
        field_name="test_mode",
        help_text="test mode flag",
    )

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

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(Q(options__has_key=value))

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(Q(metadata__values__contains=value))
