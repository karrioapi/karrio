import typing

import django.db.models as django_models
import karrio.server.filters as filters
import karrio.server.openapi as openapi
import karrio.server.shipping.models as models


class ShippingMethodFilters(filters.FilterSet):
    search = filters.CharFilter(
        method="search_filter",
        help_text="shipping method' search",
    )
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    parameters = [
        openapi.OpenApiParameter(
            "search",
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
    ]

    class Meta:
        model = models.ShippingMethod
        fields: typing.List[str] = []

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            django_models.Q(name__icontains=value)
            | django_models.Q(slug__icontains=value)
            | django_models.Q(description__icontains=value)
        )