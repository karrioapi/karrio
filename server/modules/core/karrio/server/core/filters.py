import typing
from drf_yasg import openapi
from django.db.models import Q
from django_filters import rest_framework as filters

from karrio.server.core import dataunits
from karrio.server.core import serializers
import karrio.server.manager.models as manager
import karrio.server.manager.models as models
import karrio.server.core.models as core


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ShipmentFilters(filters.FilterSet):
    address = filters.CharFilter(
        field_name="recipient__address_line1",
        lookup_expr="icontains",
        help_text="shipment recipient address line",
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
    carrier_name = filters.MultipleChoiceFilter(
        method="carrier_filter",
        choices=[(c, c) for c in dataunits.CARRIER_NAMES],
        help_text="carrier_name used to fulfill the shipment",
    )
    reference = filters.CharFilter(
        field_name="reference",
        lookup_expr="icontains",
        help_text="a shipment reference",
    )
    service = CharInFilter(
        method="service_filter",
        field_name="selected_rate__service",
        lookup_expr="in",
        help_text="preferred carrier services.",
    )
    status = filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.ShipmentStatus)],
        help_text="shipment statuses.",
    )
    option_key = CharInFilter(
        field_name="options",
        method="option_key_filter",
        help_text="shipment option keys.",
    )
    option_value = filters.CharFilter(
        field_name="options",
        method="option_value_filter",
        help_text="shipment option value",
    )
    metadata_key = CharInFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="shipment metadata keys.",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="shipment metadata value",
    )
    test_mode = filters.BooleanFilter(
        field_name="test_mode",
        help_text="test mode flag",
    )

    class Meta:
        model = manager.Shipment
        fields: typing.List[str] = []

    def carrier_filter(self, queryset, name, values):
        _filters = [
            Q(
                **{
                    f"selected_rate_carrier__{value.replace('_', '')}settings__isnull": False
                }
            )
            for value in values
        ]
        query = Q(meta__rate_provider__in=values)

        for item in _filters:
            query |= item

        return queryset.filter(query)

    def option_key_filter(self, queryset, name, value):
        return queryset.filter(Q(options__has_keys=value))

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

    def service_filter(self, queryset, name, values):
        return queryset.filter(Q(selected_rate__service__in=values))


class ShipmentModeFilter(serializers.Serializer):
    test = serializers.FlagField(
        required=False,
        allow_null=True,
        default=None,
        help_text="Create shipment in test or live mode",
    )


class TrackerFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    carrier_name = filters.MultipleChoiceFilter(
        method="carrier_filter",
        choices=[(c, c) for c in dataunits.CARRIER_NAMES],
    )
    status = filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.TrackerStatus)],
    )
    test_mode = filters.BooleanFilter(field_name="test_mode")

    class Meta:
        model = manager.Tracking
        fields: typing.List[str] = []

    def carrier_filter(self, queryset, name, values):
        _filters = [
            Q(**{f"tracking_carrier__{value.replace('_', '')}settings__isnull": False})
            for value in values
        ]
        query = _filters.pop()

        for item in _filters:
            query |= item

        return queryset.filter(query)


class LogFilter(filters.FilterSet):
    api_endpoint = filters.CharFilter(field_name="path", lookup_expr="icontains")
    date_after = filters.DateTimeFilter(field_name="requested_at", lookup_expr="gte")
    date_before = filters.DateTimeFilter(field_name="requested_at", lookup_expr="lte")
    entity_id = filters.CharFilter(method="entity_filter", field_name="response")
    method = filters.MultipleChoiceFilter(
        field_name="method",
        choices=[
            ("GET", "GET"),
            ("POST", "POST"),
            ("PATCH", "PATCH"),
            ("DELETE", "DELETE"),
        ],
    )
    status = filters.ChoiceFilter(
        method="status_filter",
        choices=[("succeeded", "succeeded"), ("failed", "failed")],
    )
    status_code = filters.TypedMultipleChoiceFilter(
        coerce=int,
        field_name="status_code",
        choices=[(s, s) for s in serializers.HTTP_STATUS],
    )

    class Meta:
        model = core.APILog
        fields: typing.List[str] = []

    def status_filter(self, queryset, name, value):
        if value == "succeeded":
            return queryset.filter(status_code__range=[200, 399])
        elif value == "failed":
            return queryset.filter(status_code__range=[400, 599])

        return queryset

    def entity_filter(self, queryset, name, value):
        return queryset.filter(response__icontains=value)


class PickupFilters(filters.FilterSet):
    parameters = [
        openapi.Parameter("test_mode", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
    ]

    class Meta:
        model = models.Pickup
        fields = ["test_mode"]
