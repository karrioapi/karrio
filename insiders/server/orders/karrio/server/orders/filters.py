from django.db.models import Q
from django_filters import rest_framework as filters

from karrio.server.core.filters import CharInFilter
from karrio.server.orders import serializers
import karrio.server.orders.models as models


class OrderFilters(filters.FilterSet):
    address = filters.CharFilter(
        method="address_filter",
        help_text="customer address line",
    )
    id = CharInFilter(
        field_name="id",
        method="id_filter",
        help_text="id(s).",
    )
    order_id = CharInFilter(
        field_name="order_id",
        method="order_id_filter",
        help_text="source order order_id(s).",
    )
    source = CharInFilter(
        field_name="source",
        method="source_filter",
        help_text="order source(s).",
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
        help_text="order statuses.",
    )
    option_key = CharInFilter(
        field_name="options",
        method="option_key_filter",
        help_text="order option keys.",
    )
    option_value = filters.CharFilter(
        field_name="options",
        method="option_value_filter",
        help_text="order option value",
    )
    metadata_key = CharInFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="order metadata keys.",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="order metadata value",
    )

    class Meta:
        model = models.Order
        fields: list = []

    def address_filter(self, queryset, name, value):
        return queryset.filter(
            Q(shipping_to__address_line1__icontains=value)
            | Q(shipping_to__address_line2__icontains=value)
            | Q(shipping_to__postal_code__icontains=value)
            | Q(shipping_to__person_name__icontains=value)
            | Q(shipping_to__company_name__icontains=value)
            | Q(shipping_to__city__icontains=value)
            | Q(shipping_to__email__icontains=value)
            | Q(shipping_to__phone_number__icontains=value)
        )

    def id_filter(self, queryset, name, value):
        return queryset.filter(Q(id__in=value))

    def order_id_filter(self, queryset, name, value):
        return queryset.filter(Q(order_id__in=value))

    def source_filter(self, queryset, name, value):
        return queryset.filter(Q(source__in=value))

    def option_key_filter(self, queryset, name, value):
        return queryset.filter(options__has_keys=value)

    def option_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "options")
                if value in (o.get("options") or {}).values()
            ]
        )

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(metadata__has_keys=value)

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "metadata")
                if value in (o.get("metadata") or {}).values()
            ]
        )
