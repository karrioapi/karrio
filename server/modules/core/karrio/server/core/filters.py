import typing
from django.db.models import Q
from django.conf import settings

import karrio.server.core.serializers as serializers
import karrio.server.core.dataunits as dataunits
import karrio.server.tracing.models as tracing
import karrio.server.core.models as core
import karrio.server.filters as filters
import karrio.server.openapi as openapi


class CarrierFilters(filters.FilterSet):

    carrier_name = filters.MultipleChoiceFilter(
        method="carrier_filter",
        choices=[(c, c) for c in dataunits.CARRIER_NAMES],
        help_text=f"""
        carrier_name used to fulfill the shipment
        Values: {', '.join([f"`{c}`" for c in dataunits.CARRIER_NAMES])}
        """,
    )
    active = filters.BooleanFilter(
        help_text="This flag indicates whether to return active carriers only",
    )
    system_only = filters.BooleanFilter(
        required=False,
        default=False,
        help_text="This flag indicates that only system carriers should be returned",
    )

    parameters = [
        openapi.OpenApiParameter(
            "action",
            type=openapi.OpenApiTypes.BOOL,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "system_only",
            type=openapi.OpenApiTypes.BOOL,
            location=openapi.OpenApiParameter.QUERY,
        ),
    ]


class ShipmentFilters(filters.FilterSet):
    address = filters.CharFilter(
        method="address_filter",
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
        help_text=f"""
        carrier_name used to fulfill the shipment
        Values: {', '.join([f"`{c}`" for c in dataunits.CARRIER_NAMES])}
        """,
    )
    reference = filters.CharFilter(
        field_name="reference",
        lookup_expr="icontains",
        help_text="a shipment reference",
    )
    service = filters.CharInFilter(
        method="service_filter",
        field_name="selected_rate__service",
        help_text="preferred carrier services.",
    )
    status = filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.ShipmentStatus)],
        help_text=f"""
        shipment status
        Values: {', '.join([f"`{s.name}`" for s in list(serializers.ShipmentStatus)])}
        """,
    )
    option_key = filters.CharInFilter(
        field_name="options",
        method="option_key_filter",
        help_text="shipment option keys.",
    )
    option_value = filters.CharFilter(
        field_name="options",
        method="option_value_filter",
        help_text="shipment option value",
    )
    metadata_key = filters.CharInFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="shipment metadata keys.",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="shipment metadata value",
    )
    tracking_number = filters.CharFilter(
        field_name="tracking_number", lookup_expr="icontains"
    )
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="shipment' keyword and indexes search",
    )

    parameters = [
        openapi.OpenApiParameter(
            "address",
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
            "carrier_name",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            enum=[c for c in dataunits.CARRIER_NAMES],
        ),
        openapi.OpenApiParameter(
            "reference",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "service",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "status",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            enum=[c.value for c in list(serializers.ShipmentStatus)],
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
            "metadata_value",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "tracking_number",
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
        import karrio.server.manager.models as manager

        model = manager.Shipment
        fields: typing.List[str] = []

    def address_filter(self, queryset, name, value):
        if "postgres" in settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "recipient__address_line1",
                    "recipient__address_line2",
                    "recipient__postal_code",
                    "recipient__person_name",
                    "recipient__company_name",
                    "recipient__city",
                    "recipient__email",
                    "recipient__phone_number",
                )
            ).filter(search=value)

        return queryset.filter(
            Q(recipient__address_line1__icontains=value)
            | Q(recipient__address_line2__icontains=value)
            | Q(recipient__postal_code__icontains=value)
            | Q(recipient__person_name__icontains=value)
            | Q(recipient__company_name__icontains=value)
            | Q(recipient__country_code__icontains=value)
            | Q(recipient__city__icontains=value)
            | Q(recipient__email__icontains=value)
            | Q(recipient__phone_number__icontains=value)
        )

    def keyword_filter(self, queryset, name, value):
        if "postgres" in settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "reference",
                    "tracking_number",
                    "recipient__address_line1",
                    "recipient__address_line2",
                    "recipient__postal_code",
                    "recipient__person_name",
                    "recipient__company_name",
                    "recipient__city",
                    "recipient__email",
                    "recipient__phone_number",
                )
            ).filter(search=value)

        return queryset.filter(
            Q(recipient__address_line1__icontains=value)
            | Q(recipient__address_line2__icontains=value)
            | Q(recipient__postal_code__icontains=value)
            | Q(recipient__person_name__icontains=value)
            | Q(recipient__company_name__icontains=value)
            | Q(recipient__country_code__icontains=value)
            | Q(recipient__city__icontains=value)
            | Q(recipient__email__icontains=value)
            | Q(recipient__phone_number__icontains=value)
            | Q(tracking_number__icontains=value)
            | Q(reference__icontains=value)
        )

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


class TrackerFilters(filters.FilterSet):
    tracking_number = filters.CharFilter(
        field_name="tracking_number",
        lookup_expr="icontains",
        help_text="a tracking number",
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
        help_text=f"""
        carrier_name used to fulfill the shipment
        Values: {', '.join([f"`{c}`" for c in dataunits.CARRIER_NAMES])}
        """,
    )
    status = filters.MultipleChoiceFilter(
        field_name="status",
        choices=[(c.value, c.value) for c in list(serializers.TrackerStatus)],
        help_text=f"""
        tracker status
        Values: {', '.join([f"`{s.name}`" for s in list(serializers.TrackerStatus)])}
        """,
    )

    parameters = [
        openapi.OpenApiParameter(
            "tracking_number",
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
            "carrier_name",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            enum=[c for c in dataunits.CARRIER_NAMES],
        ),
        openapi.OpenApiParameter(
            "status",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            enum=[c.value for c in list(serializers.TrackerStatus)],
        ),
    ]

    class Meta:
        import karrio.server.manager.models as manager

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
    entity_id = filters.CharFilter(field_name="entity_id")
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
        model = core.APILogIndex
        fields: typing.List[str] = []

    def status_filter(self, queryset, name, value):
        if value == "succeeded":
            return queryset.filter(status_code__range=[200, 399])
        elif value == "failed":
            return queryset.filter(status_code__range=[400, 599])

        return queryset


class TracingRecordFilter(filters.FilterSet):
    key = filters.CharFilter(
        field_name="key",
        help_text="the tacing log key.",
    )
    request_log_id = filters.NumberFilter(
        method="request_log_id_filter",
        field_name="meta__request_log_id",
        lookup_expr="icontains",
        help_text="related request API log.",
    )
    date_after = filters.DateTimeFilter(field_name="requested_at", lookup_expr="gte")
    date_before = filters.DateTimeFilter(field_name="requested_at", lookup_expr="lte")

    class Meta:
        model = tracing.TracingRecord
        fields: list = []

    def request_log_id_filter(self, queryset, name, value):
        return queryset.filter(meta__request_log_id__icontains=value)


class UploadRecordFilter(filters.FilterSet):
    date_after = filters.DateTimeFilter(field_name="requested_at", lookup_expr="gte")
    date_before = filters.DateTimeFilter(field_name="requested_at", lookup_expr="lte")

    class Meta:
        import karrio.server.manager.models as manager

        model = manager.DocumentUploadRecord
        fields: list = []


class PickupFilters(filters.FilterSet):
    parameters: list = []

    class Meta:
        import karrio.server.manager.models as manager

        model = manager.Pickup
        fields: list = []
