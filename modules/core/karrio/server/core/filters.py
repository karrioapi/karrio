import typing
import django.conf as conf
import django.db.models as models
import django.contrib.auth as auth

import karrio.server.core.serializers as serializers
import karrio.server.core.dataunits as dataunits
import karrio.server.tracing.models as tracing
import karrio.server.core.models as core
import karrio.server.filters as filters
import karrio.server.openapi as openapi

User = auth.get_user_model()


class UserFilter(filters.FilterSet):
    id = filters.CharFilter(field_name="id", help_text="user id")
    email = filters.CharFilter(field_name="email", help_text="user email")
    is_active = filters.BooleanFilter(
        help_text="This flag indicates whether to return active carriers only",
    )
    is_staff = filters.BooleanFilter(
        help_text="This flag indicates whether to return active carriers only",
    )
    is_superuser = filters.BooleanFilter(
        help_text="This flag indicates whether to return active carriers only",
    )
    order_by = filters.OrderingFilter(
        fields=(
            ("is_active", "is_active"),
            ("is_staff", "is_staff"),
            ("is_superuser", "is_superuser"),
            ("date_joined", "date_joined"),
            ("last_login", "last_login"),
        ),
    )

    class Meta:
        model = User
        fields: list = []


class CarrierFilters(filters.FilterSet):
    carrier_name = filters.CharFilter(
        help_text=f"""
        carrier_name used to fulfill the shipment
        Values: {', '.join([f"`{c}`" for c in dataunits.CARRIER_NAMES])}
        """,
    )
    active = filters.BooleanFilter(
        help_text="This flag indicates whether to return active carriers only",
    )
    system_only = filters.BooleanFilter(
        help_text="This flag indicates that only system carriers should be returned",
    )
    metadata_key = filters.CharFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="connection metadata keys.",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="connection metadata value.",
    )

    parameters = [
        openapi.OpenApiParameter(
            "carrier_name",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            description=(
                "The unique carrier slug. <br/>"
                f"Values: {', '.join([f'`{c}`' for c in dataunits.CARRIER_NAMES])}"
            ),
        ),
        openapi.OpenApiParameter(
            "active",
            type=openapi.OpenApiTypes.BOOL,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "system_only",
            type=openapi.OpenApiTypes.BOOL,
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
    ]

    class Meta:
        import karrio.server.providers.models as providers

        model = providers.Carrier
        fields: typing.List[str] = []

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(metadata__has_key=value)

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "metadata")
                if value in (o.get("metadata") or {}).values()
            ]
        )


class CarrierConnectionFilter(filters.FilterSet):
    carrier_name = filters.CharFilter(
        help_text=f"""
        carrier_name used to fulfill the shipment
        Values: {', '.join([f"`{c}`" for c in dataunits.CARRIER_NAMES])}
        """,
    )
    active = filters.BooleanFilter(
        help_text="This flag indicates whether to return active carriers only",
    )
    system_only = filters.BooleanFilter(
        help_text="This flag indicates that only system carriers should be returned",
    )
    metadata_key = filters.CharFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="connection metadata keys.",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="connection metadata value.",
    )

    parameters = [
        openapi.OpenApiParameter(
            "carrier_name",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            description=(
                "The unique carrier slug. <br/>"
                f"Values: {', '.join([f'`{c}`' for c in dataunits.CARRIER_NAMES])}"
            ),
        ),
        openapi.OpenApiParameter(
            "active",
            type=openapi.OpenApiTypes.BOOL,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "system_only",
            type=openapi.OpenApiTypes.BOOL,
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
    ]

    class Meta:
        import karrio.server.providers.models as providers

        model = providers.Carrier
        fields: typing.List[str] = []

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(metadata__has_key=value)

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "metadata")
                if value in (o.get("metadata") or {}).values()
            ]
        )


class ShipmentFilters(filters.FilterSet):
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="shipment' keyword and indexes search",
    )
    tracking_number = filters.CharFilter(
        field_name="tracking_number", lookup_expr="icontains"
    )
    id = filters.CharInFilter(
        field_name="id",
        lookup_expr="in",
        help_text="id(s).",
    )
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
    option_key = filters.CharFilter(
        field_name="options",
        method="option_key_filter",
        help_text="shipment option keys.",
    )
    option_value = filters.CharFilter(
        field_name="options",
        method="option_value_filter",
        help_text="shipment option value",
    )
    metadata_key = filters.CharFilter(
        field_name="metadata",
        method="metadata_key_filter",
        help_text="shipment metadata keys.",
    )
    metadata_value = filters.CharFilter(
        field_name="metadata",
        method="metadata_value_filter",
        help_text="shipment metadata value",
    )
    meta_key = filters.CharFilter(
        field_name="meta",
        method="meta_key_filter",
        help_text="shipment meta keys.",
    )
    meta_value = filters.CharFilter(
        field_name="meta",
        method="meta_value_filter",
        help_text="shipment meta value",
    )
    has_tracker = filters.BooleanFilter(
        field_name="shipment_tracker",
        help_text="shipment has tracker",
        method="has_tracker_filter",
    )
    has_manifest = filters.BooleanFilter(
        field_name="manifest",
        help_text="shipment has manifest",
        method="has_manifest_filter",
    )

    parameters = [
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
        openapi.OpenApiParameter(
            "id",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
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
            description=(
                "The unique carrier slug. <br/>"
                f"Values: {', '.join([f'`{c}`' for c in dataunits.CARRIER_NAMES])}"
            ),
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
            description=(
                "Valid shipment status. <br/>"
                f"Values: {', '.join([f'`{c.value}`' for c in list(serializers.ShipmentStatus)])}"
            ),
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
            "meta_key",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "meta_value",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "has_tracker",
            type=openapi.OpenApiTypes.BOOL,
            location=openapi.OpenApiParameter.QUERY,
        ),
        openapi.OpenApiParameter(
            "has_manifest",
            type=openapi.OpenApiTypes.BOOL,
            location=openapi.OpenApiParameter.QUERY,
        ),
    ]

    class Meta:
        import karrio.server.manager.models as manager

        model = manager.Shipment
        fields: typing.List[str] = []

    def address_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "recipient__address_line1",
                    "recipient__address_line2",
                    "recipient__postal_code",
                    "recipient__person_name",
                    "recipient__company_name",
                    "recipient__country_code",
                    "recipient__city",
                    "recipient__email",
                    "recipient__phone_number",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value)
            | models.Q(recipient__address_line1__icontains=value)
            | models.Q(recipient__address_line2__icontains=value)
            | models.Q(recipient__postal_code__icontains=value)
            | models.Q(recipient__person_name__icontains=value)
            | models.Q(recipient__company_name__icontains=value)
            | models.Q(recipient__country_code__icontains=value)
            | models.Q(recipient__city__icontains=value)
            | models.Q(recipient__email__icontains=value)
            | models.Q(recipient__phone_number__icontains=value)
        )

    def keyword_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "id",
                    "reference",
                    "tracking_number",
                    "recipient__address_line1",
                    "recipient__address_line2",
                    "recipient__postal_code",
                    "recipient__person_name",
                    "recipient__company_name",
                    "recipient__country_code",
                    "recipient__city",
                    "recipient__email",
                    "recipient__phone_number",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value)
            | models.Q(recipient__address_line1__icontains=value)
            | models.Q(recipient__address_line2__icontains=value)
            | models.Q(recipient__postal_code__icontains=value)
            | models.Q(recipient__person_name__icontains=value)
            | models.Q(recipient__company_name__icontains=value)
            | models.Q(recipient__country_code__icontains=value)
            | models.Q(recipient__city__icontains=value)
            | models.Q(recipient__email__icontains=value)
            | models.Q(recipient__phone_number__icontains=value)
            | models.Q(tracking_number__icontains=value)
            | models.Q(reference__icontains=value)
        )

    def carrier_filter(self, queryset, name, values):
        _filters = [
            models.Q(selected_rate_carrier__carrier_code=value) for value in values
        ]
        query = models.Q(meta__rate_provider__in=values)

        for item in _filters:
            query |= item

        return queryset.filter(query)

    def service_filter(self, queryset, name, values):
        return queryset.filter(models.Q(selected_rate__service__in=values))

    def option_key_filter(self, queryset, name, value):
        return queryset.filter(models.Q(options__has_key=value))

    def option_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "options")
                if value in (o.get("options") or {}).values()
            ]
        )

    def metadata_key_filter(self, queryset, name, value):
        return queryset.filter(metadata__has_key=value)

    def metadata_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "metadata")
                if value in (o.get("metadata") or {}).values()
            ]
        )

    def meta_key_filter(self, queryset, name, value):
        return queryset.filter(meta__has_key=value)

    def meta_value_filter(self, queryset, name, value):
        return queryset.filter(
            id__in=[
                o["id"]
                for o in queryset.values("id", "meta")
                if value in map(str, (o.get("meta") or {}).values())
            ]
        )

    def has_tracker_filter(self, queryset, name, value):
        return queryset.filter(shipment_tracker__isnull=not value)

    def has_manifest_filter(self, queryset, name, value):
        return queryset.filter(manifest__isnull=not value)


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
            description=(
                "The unique carrier slug. <br/>"
                f"Values: {', '.join([f'`{c}`' for c in dataunits.CARRIER_NAMES])}"
            ),
        ),
        openapi.OpenApiParameter(
            "status",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            description=(
                "Valid tracker status. <br/>"
                f"Values: {', '.join([f'`{c.value}`' for c in list(serializers.TrackerStatus)])}"
            ),
        ),
    ]

    class Meta:
        import karrio.server.manager.models as manager

        model = manager.Tracking
        fields: typing.List[str] = []

    def carrier_filter(self, queryset, name, values):
        _filters = [models.Q(tracking_carrier__carrier_code=value) for value in values]
        query = _filters.pop()

        for item in _filters:
            query |= item

        return queryset.filter(query)


class LogFilter(filters.FilterSet):
    api_endpoint = filters.CharFilter(field_name="path", lookup_expr="icontains")
    remote_addr = filters.CharFilter(field_name="remote_addr", lookup_expr="exact")
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
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="search in entity_id and data",
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

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(entity_id__icontains=value) |
            models.Q(data__icontains=value) |
            models.Q(path__icontains=value) |
            models.Q(remote_addr__icontains=value) |
            models.Q(host__icontains=value) |
            models.Q(method__icontains=value)
        )

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
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="search in key and meta",
    )

    class Meta:
        model = tracing.TracingRecord
        fields: list = []

    def request_log_id_filter(self, queryset, name, value):
        return queryset.filter(meta__request_log_id=value)

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(key__icontains=value) |
            models.Q(meta__icontains=value)
        )


class UploadRecordFilter(filters.FilterSet):
    shipment_id = filters.CharFilter(
        field_name="shipment__id", help_text="related shipment id"
    )
    created_after = filters.DateTimeFilter(field_name="requested_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(
        field_name="requested_at", lookup_expr="lte"
    )

    parameters = [
        openapi.OpenApiParameter(
            "shipment_id",
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
        import karrio.server.manager.models as manager

        model = manager.DocumentUploadRecord
        fields: list = []


class PickupFilters(filters.FilterSet):
    parameters: list = []

    class Meta:
        import karrio.server.manager.models as manager

        model = manager.Pickup
        fields: list = []


class RateSheetFilter(filters.FilterSet):
    keyword = filters.CharFilter(
        method="keyword_filter",
        help_text="rate sheet keyword and indexes search",
    )

    class Meta:
        import karrio.server.providers.models as providers

        model = providers.RateSheet
        fields: typing.List[str] = []

    def keyword_filter(self, queryset, name, value):
        if "postgres" in conf.settings.DB_ENGINE:
            from django.contrib.postgres.search import SearchVector

            return queryset.annotate(
                search=SearchVector(
                    "id",
                    "name",
                    "slug",
                    "carrier_name",
                )
            ).filter(search=value)

        return queryset.filter(
            models.Q(id__icontains=value)
            | models.Q(name__icontains=value)
            | models.Q(slug__icontains=value)
            | models.Q(carrier_name__icontains=value)
        )


class ManifestFilters(filters.FilterSet):
    id = filters.CharInFilter(
        field_name="id",
        lookup_expr="in",
        help_text="id(s).",
    )
    carrier_name = filters.MultipleChoiceFilter(
        method="carrier_filter",
        choices=[(c, c) for c in dataunits.CARRIER_NAMES],
        help_text=f"""
        carrier_name used to fulfill the shipment
        Values: {', '.join([f"`{c}`" for c in dataunits.CARRIER_NAMES])}
        """,
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

    parameters = [
        openapi.OpenApiParameter(
            "carrier_name",
            type=openapi.OpenApiTypes.STR,
            location=openapi.OpenApiParameter.QUERY,
            description=(
                "The unique carrier slug. <br/>"
                f"Values: {', '.join([f'`{c}`' for c in dataunits.CARRIER_NAMES])}"
            ),
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
        import karrio.server.manager.models as manager

        model = manager.Manifest
        fields: typing.List[str] = []

    def carrier_filter(self, queryset, name, values):
        _filters = [models.Q(manifest_carrier__carrier_code=value) for value in values]
        query = _filters.pop()

        for item in _filters:
            query |= item

        return queryset.filter(query)
