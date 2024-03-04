from django.db.models import Q
from django.conf import settings

import karrio.server.filters as filters
import karrio.server.orders.serializers as serializers
import karrio.server.orders.models as models
import karrio.server.openapi as openapi


class OrderFilters(filters.FilterSet):
    address = filters.CharFilter(
        method="address_filter",
        help_text="customer address line",
    )
    id = filters.CharInFilter(
        field_name="id",
        lookup_expr="in",
        help_text="id(s).",
    )
    order_id = filters.CharInFilter(
        field_name="order_id",
        method="order_id_filter",
        help_text="source order order_id(s).",
    )
    source = filters.CharInFilter(
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
    option_key = filters.CharInFilter(
        field_name="options",
        method="option_key_filter",
        help_text="order option keys.",
    )
    option_value = filters.CharFilter(
        field_name="options",
        method="option_value_filter",
        help_text="order option value",
    )
    metadata_key = filters.CharInFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="order metadata keys.",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="order metadata value",
    )
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="order' keyword and indexes search",
    )

    parameters = [
        openapi.OpenApiParameter(
            "address",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "id",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "order_id",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "source",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "created_after",
            type=openapi.OpenApiTypes.DATETIME,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "created_before",
            type=openapi.OpenApiTypes.DATETIME,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "status",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            enum=[c.value for c in list(serializers.OrderStatus)],
        ),
        openapi.OpenApiParameter(
            "option_key",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "option_value",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "metadata_key",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "metadata_value",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "keyword",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
    ]

    class Meta:
        model = models.Order
        fields: list = []

    def keyword_filter(self, queryset, name, value):
        if "postgres" in settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "shipping_to__address_line1",
                    "shipping_to__address_line2",
                    "shipping_to__postal_code",
                    "shipping_to__person_name",
                    "shipping_to__company_name",
                    "shipping_to__city",
                    "shipping_to__email",
                    "shipping_to__phone_number",
                    "order_id",
                    "source",
                    "id",
                )
            ).filter(search=value)

        return queryset.filter(
            Q(shipping_to__address_line1__icontains=value)
            | Q(shipping_to__address_line2__icontains=value)
            | Q(shipping_to__postal_code__icontains=value)
            | Q(shipping_to__person_name__icontains=value)
            | Q(shipping_to__company_name__icontains=value)
            | Q(shipping_to__city__icontains=value)
            | Q(shipping_to__email__icontains=value)
            | Q(shipping_to__phone_number__icontains=value)
            | Q(order_id__icontains=value)
            | Q(source__icontains=value)
            | Q(id__icontains=value)
        )

    def address_filter(self, queryset, name, value):
        if "postgres" in settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "shipping_to__address_line1",
                    "shipping_to__address_line2",
                    "shipping_to__postal_code",
                    "shipping_to__person_name",
                    "shipping_to__company_name",
                    "shipping_to__city",
                    "shipping_to__email",
                    "shipping_to__phone_number",
                )
            ).filter(search=value)

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
