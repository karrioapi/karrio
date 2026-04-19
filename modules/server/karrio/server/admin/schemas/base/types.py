import datetime
import typing

import karrio.lib as lib
import karrio.server.admin.schemas.base.inputs as inputs
import karrio.server.admin.utils as admin
import karrio.server.conf as conf
import karrio.server.core.filters as filters
import karrio.server.graph.schemas.base.types as base
import karrio.server.graph.utils as utils
import karrio.server.iam.models as iam
import karrio.server.manager.models as manager
import karrio.server.pricing.models as pricing
import karrio.server.providers.models as providers
import strawberry
from django.utils import timezone
from strawberry.types import Info

PRIVATE_CONFIGS = [
    "EMAIL_USE_TLS",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "EMAIL_HOST",
    "EMAIL_PORT",
    "EMAIL_FROM_ADDRESS",
    "GOOGLE_CLOUD_API_KEY",
    "CANADAPOST_ADDRESS_COMPLETE_API_KEY",
]


@strawberry.type
class SystemUserType(base.UserType):
    id: int

    @strawberry.field
    def permissions(self: iam.User, info: Info) -> list[str] | None:
        return self.permissions

    @strawberry.field
    def metadata(self: iam.User) -> utils.JSON | None:
        try:
            return lib.to_dict(self.metadata)
        except Exception:
            return self.metadata

    @staticmethod
    @utils.authentication_required
    def me(info: Info) -> "SystemUserType":
        return iam.User.objects.get(id=info.context.request.user.id)

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info: Info,
        email: str = strawberry.UNSET,
    ) -> typing.Optional["SystemUserType"]:
        queryset = iam.User.objects.filter(email=email, is_staff=True)
        return queryset.first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info: Info,
        filter: inputs.UserFilter | None = strawberry.UNSET,
    ) -> utils.Connection["SystemUserType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.UserFilter()
        queryset = filters.UserFilter(_filter.to_dict(), iam.User.objects.filter(is_staff=True)).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class PermissionGroupType:
    id: int
    name: str

    @strawberry.field
    def permissions(self: iam.Group) -> list[str] | None:
        return self.permissions.all().values_list("name", flat=True)

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info: Info,
        filter: inputs.PermissionGroupFilter | None = strawberry.UNSET,
    ) -> utils.Connection["PermissionGroupType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.PermissionGroupFilter()
        queryset = iam.Group.objects.filter()

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class SystemCarrierConnectionType(base.CarrierConnectionType):
    """Admin type for system carrier connections.

    Note: Includes credentials field for admin management (not exposed to regular users).
    This type now maps to the SystemConnection model (admin-managed platform connections).
    """

    object_type: str | None

    @strawberry.field
    def credentials(self: providers.SystemConnection, info: Info) -> utils.JSON:
        """Get decrypted credentials for admin management."""
        return self.get_credentials()

    @strawberry.field
    def config(self: providers.SystemConnection, info: Info) -> utils.JSON | None:
        """Return the raw system-connection config for admin editing.

        Overrides the base resolver which returns None for SystemConnection to
        prevent billing numbers leaking via the tenant graph. Admin staff need
        the full config to manage billing numbers, label_type, default values, etc.
        """
        return getattr(self, "config", None)

    @strawberry.field
    def usage(
        self: providers.SystemConnection,
        info: Info,
        filter: utils.UsageFilter | None = strawberry.UNSET,
    ) -> "ResourceUsageType":
        # Check for batch-precomputed usage on request context (avoids N+1)
        _cache = getattr(info.context.request, "_usage_cache", None)
        if _cache and self.id in _cache:
            return _cache[self.id]

        # Fallback for single-item resolve (e.g. resolve() not resolve_list())
        base_filter = filter.to_dict() if not utils.is_unset(filter) else {}
        enhanced_filter = utils.UsageFilter(
            date_after=base_filter.get("date_after", strawberry.UNSET),
            date_before=base_filter.get("date_before", strawberry.UNSET),
            omit=base_filter.get("omit", strawberry.UNSET),
        )

        import types as python_types

        enhanced_filter_dict = enhanced_filter.to_dict()
        enhanced_filter_dict["carrier_connection_id"] = self.id

        mock_filter = python_types.SimpleNamespace(**enhanced_filter_dict)
        mock_filter.to_dict = lambda: enhanced_filter_dict

        return ResourceUsageType.resolve_usage(info, filter=mock_filter)

    @strawberry.field
    def shipments(
        self: providers.SystemConnection,
        info: Info,
        filter: inputs.base.ShipmentFilter | None = strawberry.UNSET,
    ) -> utils.Connection[base.ShipmentType]:
        _filter = filter if not utils.is_unset(filter) else inputs.base.ShipmentFilter()
        _filter_data = _filter.to_dict()
        # Query shipments that used this system connection via brokered connections
        brokered_ids = list(
            providers.BrokeredConnection.objects.filter(system_connection=self).values_list("id", flat=True)
        )
        # Include both direct system connection usage and brokered usage
        queryset = filters.ShipmentFilters(
            _filter_data,
            manager.Shipment.objects.filter(selected_rate__meta__connection_id__in=[self.id] + brokered_ids),
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info, id: str) -> typing.Optional["SystemCarrierConnectionType"]:
        # Now queries SystemConnection model directly
        return providers.SystemConnection.objects.filter(
            id=id,
            test_mode=getattr(info.context.request, "test_mode", False),
        ).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info: Info,
        filter: inputs.base.CarrierFilter | None = strawberry.UNSET,
    ) -> utils.Connection["SystemCarrierConnectionType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.base.CarrierFilter()
        _filter_data = _filter.to_dict()
        _test_mode = getattr(info.context.request, "test_mode", False)

        # Build queryset from SystemConnection model
        queryset = providers.SystemConnection.objects.filter(test_mode=_test_mode)

        # Apply common filters
        if _filter_data.get("active") is not None:
            queryset = queryset.filter(active=_filter_data["active"])
        if _filter_data.get("carrier_name"):
            queryset = queryset.filter(carrier_code=_filter_data["carrier_name"])

        # Batch-prefetch usage for all connections to avoid N+1 queries
        connection_ids = list(queryset.values_list("id", flat=True))
        if connection_ids:
            info.context.request._usage_cache = ResourceUsageType.batch_resolve_usage(
                info, connection_ids=connection_ids
            )

        return utils.paginated_connection(queryset)


def _ensure_aware(value):
    """Coerce a datetime / ISO-string into a tz-aware datetime.

    Admin usage-stat queries feed `created_at__gte=` / `__lte=` on
    Fee/Shipment DateTimeFields, which are tz-aware. Naive values slip
    through when the GraphQL input carries an ISO string without a
    trailing 'Z' / offset — Django then emits the familiar
    ``DateTimeField received a naive datetime`` RuntimeWarning on every
    matching row. Normalise once at the query boundary.
    """
    if value is None:
        return None
    if isinstance(value, str):
        parsed = timezone.datetime.fromisoformat(value.replace("Z", "+00:00"))
        value = parsed
    if isinstance(value, datetime.datetime) and timezone.is_naive(value):
        return timezone.make_aware(value, timezone.get_current_timezone())
    return value


def _bulk_load_constance_config(keys):
    """Bulk load constance configuration values to avoid N+1 queries."""
    from constance.codecs import loads
    from django.apps import apps

    Constance = apps.get_model("constance", "Constance")

    # Add prefix to keys (matching constance backend behavior)
    prefix = conf.settings.CONSTANCE_DATABASE_PREFIX
    prefixed_keys = [f"{prefix}{key}" for key in keys]

    # Use Django ORM to bulk fetch all values in a single query
    constance_values = Constance.objects.filter(key__in=prefixed_keys).values("key", "value")

    # Build dict mapping unprefixed key to deserialized value
    values_dict = {}
    for item in constance_values:
        # Remove prefix from key
        unprefixed_key = item["key"].replace(prefix, "", 1)
        # Deserialize the value
        values_dict[unprefixed_key] = loads(item["value"])

    # Return values in the same order as keys, with defaults for missing keys
    result = {}
    for key in keys:
        if key in values_dict:
            result[key] = values_dict[key]
        else:
            # Get default from CONSTANCE_CONFIG
            default_value = conf.settings.CONSTANCE_CONFIG.get(key, [None])[0]
            result[key] = default_value

    return result


@strawberry.type
class InstanceConfigType:
    configs: utils.JSON | None = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info) -> "InstanceConfigType":
        if conf.settings.tenant:
            values = {k: getattr(conf.settings, k, None) for k in conf.settings.CONSTANCE_CONFIG}
        else:
            all_keys = list(conf.settings.CONSTANCE_CONFIG.keys())
            values = _bulk_load_constance_config(all_keys)

        return InstanceConfigType(configs=values)


@strawberry.type
class ConfigFieldsetType:
    name: str
    keys: list[str]

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(info: Info) -> list["ConfigFieldsetType"]:
        fieldsets = getattr(conf.settings, "CONSTANCE_CONFIG_FIELDSETS", {})
        return [ConfigFieldsetType(name=name, keys=list(keys)) for name, keys in fieldsets.items()]


@strawberry.type
class ConfigSchemaItemType:
    key: str
    description: str
    value_type: str
    default_value: str | None = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(info: Info) -> list["ConfigSchemaItemType"]:
        config = getattr(conf.settings, "CONSTANCE_CONFIG", {})
        return [
            ConfigSchemaItemType(
                key=key,
                description=definition[1] if len(definition) > 1 else "",
                value_type=type(definition[0]).__name__,
                default_value=str(definition[0]) if definition[0] is not None else None,
            )
            for key, definition in config.items()
        ]


@strawberry.type
class SystemRateSheetType(base.RateSheetType):
    id: str

    @strawberry.field
    def carriers(
        self: providers.SystemRateSheet,
    ) -> list[SystemCarrierConnectionType]:
        return self.carriers

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info: Info,
        id: str,
    ) -> typing.Optional["SystemRateSheetType"]:
        return providers.SystemRateSheet.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info: Info,
        filter: inputs.base.RateSheetFilter | None = strawberry.UNSET,
    ) -> utils.Connection["SystemRateSheetType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.base.RateSheetFilter()
        queryset = filters.SystemRateSheetFilter(_filter.to_dict(), providers.SystemRateSheet.objects.all()).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class ResourceUsageType:
    total_trackers: int | None = None
    total_shipments: int | None = None
    total_addons_charges: float | None = None
    total_shipping_spend: float | None = None
    addons_charges: list[utils.UsageStatType] | None = None
    shipping_spend: list[utils.UsageStatType] | None = None
    tracker_count: list[utils.UsageStatType] | None = None

    @staticmethod
    def batch_resolve_usage(
        info: Info,
        connection_ids: list[str],
        filter: utils.UsageFilter = strawberry.UNSET,
    ) -> dict[str, "ResourceUsageType"]:
        """Batch-compute usage for multiple connections in 4 queries total."""
        import django.db.models as models
        import django.db.models.functions as functions
        import karrio.server.manager.models as manager

        _test_mode = info.context.request.test_mode
        _filter = {
            "date_before": timezone.now(),
            "date_after": (timezone.now() - datetime.timedelta(days=30)),
            **(filter.to_dict() if not utils.is_unset(filter) else {}),
        }
        _filter["date_before"] = _ensure_aware(_filter.get("date_before"))
        _filter["date_after"] = _ensure_aware(_filter.get("date_after"))

        # Query 1: Shipment stats grouped by connection_id
        shipment_qs = (
            filters.ShipmentFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                    status__not_in=["draft", "cancelled"],
                ),
                manager.Shipment.objects.filter(
                    test_mode=_test_mode,
                    selected_rate__meta__carrier_connection_id__in=connection_ids,
                ),
            )
            .qs.annotate(
                connection_id=models.F("selected_rate__meta__carrier_connection_id"),
                date=functions.TruncDay("created_at"),
            )
            .values("connection_id", "date")
            .annotate(
                count=models.Count("id"),
                amount=functions.Coalesce(
                    models.Sum(functions.Cast("selected_rate__total_charge", models.FloatField())),
                    models.Value(0.0),
                ),
            )
            .order_by("connection_id", "-date")
        )

        # Query 2: Fee stats grouped by connection_id
        fee_qs = (
            pricing.Fee.objects.filter(
                created_at__gte=_filter["date_after"],
                created_at__lte=_filter["date_before"],
                test_mode=_test_mode,
                connection_id__in=connection_ids,
            )
            .annotate(date=functions.TruncDay("created_at"))
            .values("connection_id", "date")
            .annotate(count=models.Count("id"), amount=models.Sum("amount"))
            .order_by("connection_id", "-date")
        )

        # Query 3: Tracker stats grouped by connection_id
        tracker_qs = (
            filters.TrackerFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                ),
                manager.Tracking.objects.filter(
                    test_mode=_test_mode,
                    carrier__id__in=connection_ids,
                ),
            )
            .qs.annotate(
                connection_id=models.F("carrier__id"),
                date=functions.TruncDay("created_at"),
            )
            .values("connection_id", "date")
            .annotate(count=models.Count("id"))
            .order_by("connection_id", "-date")
        )

        # Build per-connection data from batch results
        shipment_data: dict[str, list] = {cid: [] for cid in connection_ids}
        shipment_counts: dict[str, int] = {cid: 0 for cid in connection_ids}
        for row in shipment_qs:
            cid = row["connection_id"]
            if cid in shipment_data:
                shipment_data[cid].append(row)
                shipment_counts[cid] += row["count"]

        fee_data: dict[str, list] = {cid: [] for cid in connection_ids}
        for row in fee_qs:
            cid = row["connection_id"]
            if cid in fee_data:
                fee_data[cid].append(row)

        tracker_data: dict[str, list] = {cid: [] for cid in connection_ids}
        for row in tracker_qs:
            cid = row["connection_id"]
            if cid in tracker_data:
                tracker_data[cid].append(row)

        # Assemble ResourceUsageType per connection
        result = {}
        for cid in connection_ids:
            _shipping = shipment_data[cid]
            _fees = fee_data[cid]
            _trackers = tracker_data[cid]

            total_shipping_spend = lib.to_decimal(sum((r["amount"] for r in _shipping if r["amount"] is not None), 0.0))
            total_addons_charges = lib.to_decimal(sum((r["amount"] for r in _fees if r["amount"] is not None), 0.0))
            total_trackers = sum((r["count"] for r in _trackers if r["count"] is not None), 0)

            result[cid] = ResourceUsageType(
                total_trackers=total_trackers,
                total_shipments=shipment_counts[cid],
                total_addons_charges=lib.to_decimal(total_addons_charges),
                total_shipping_spend=lib.to_decimal(total_shipping_spend),
                shipping_spend=[utils.UsageStatType.parse(r, label="shipping_spend") for r in _shipping],
                tracker_count=[utils.UsageStatType.parse(r, label="tracker_count") for r in _trackers],
                addons_charges=[utils.UsageStatType.parse(r, label="addons_charges") for r in _fees],
            )

        return result

    @staticmethod
    def resolve_usage(
        info: Info,
        filter: utils.UsageFilter = strawberry.UNSET,
    ) -> "ResourceUsageType":
        import django.db.models as models
        import django.db.models.functions as functions
        import karrio.server.manager.models as manager

        _test_mode = info.context.request.test_mode
        _test_filter = dict(test_mode=_test_mode)
        _filter = {
            "date_before": timezone.now(),
            "date_after": (timezone.now() - datetime.timedelta(days=30)),
            **filter.to_dict(),
        }
        _filter["date_before"] = _ensure_aware(_filter.get("date_before"))
        _filter["date_after"] = _ensure_aware(_filter.get("date_after"))
        _account_filter = lib.identity(dict(org__id=_filter.get("account_id")) if _filter.get("account_id") else {})
        _connection_filter = lib.identity(
            dict(selected_rate__meta__carrier_connection_id=_filter.get("carrier_connection_id"))
            if _filter.get("carrier_connection_id")
            else {}
        )
        _tracker_filter = lib.identity(
            dict(carrier__id=_filter.get("carrier_connection_id")) if _filter.get("carrier_connection_id") else {}
        )

        shipments = lib.identity(
            filters.ShipmentFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                    status__not_in=["draft", "cancelled"],
                ),
                manager.Shipment.objects.filter(
                    **{
                        **_test_filter,
                        **_connection_filter,
                        **_account_filter,
                    }
                ),
            )
        )

        shipping_spend = lib.identity(
            shipments.qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(
                count=models.Count("id"),
                amount=functions.Coalesce(
                    models.Sum(functions.Cast("selected_rate__total_charge", models.FloatField())),
                    models.Value(0.0),
                ),
            )
            .order_by("-date")
        )

        # Use Fee table for addons_charges (single indexed SQL query)
        _fee_filters = {
            "created_at__gte": _filter["date_after"],
            "created_at__lte": _filter["date_before"],
            "test_mode": _test_mode,
        }
        if _filter.get("markup_id"):
            _fee_filters["markup_id"] = _filter["markup_id"]
        if _filter.get("account_id"):
            _fee_filters["account_id"] = _filter["account_id"]
        if _filter.get("carrier_connection_id"):
            _fee_filters["connection_id"] = _filter["carrier_connection_id"]

        addons_charges = (
            pricing.Fee.objects.filter(**_fee_filters)
            .annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(count=models.Count("id"), amount=models.Sum("amount"))
            .order_by("-date")
        )

        tracker_count = (
            filters.TrackerFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                ),
                manager.Tracking.objects.filter(
                    **{
                        **_test_filter,
                        **_tracker_filter,
                        **_account_filter,
                    }
                ),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(count=models.Count("id"))
            .order_by("-date")
        )

        total_shipments = shipments.qs.count()
        total_shipping_spend = lib.to_decimal(
            sum(
                [item["amount"] for item in shipping_spend if item["amount"] is not None],
                0.0,
            )
        )
        total_addons_charges = lib.to_decimal(
            sum(
                [item["amount"] for item in addons_charges if item["amount"] is not None],
                0.0,
            )
        )
        total_trackers = sum([item["count"] for item in tracker_count if item["count"] is not None], 0)

        return ResourceUsageType(
            total_trackers=total_trackers,
            total_shipments=total_shipments,
            total_addons_charges=lib.to_decimal(total_addons_charges),
            total_shipping_spend=lib.to_decimal(total_shipping_spend),
            shipping_spend=[utils.UsageStatType.parse(item, label="shipping_spend") for item in shipping_spend],
            tracker_count=[utils.UsageStatType.parse(item, label="tracker_count") for item in tracker_count],
            addons_charges=[utils.UsageStatType.parse(item, label="addons_charges") for item in addons_charges],
        )


@strawberry.type
class MarkupType:
    """Admin GraphQL type for Markup model (formerly AddonType/Surcharge)."""

    object_type: str
    id: str
    name: str
    active: bool
    amount: float
    markup_type: str
    is_visible: bool = True
    meta: utils.JSON | None = None
    metadata: utils.JSON | None = None

    @strawberry.field
    def service_codes(self: pricing.Markup) -> list[str]:
        return self.service_codes or []

    @strawberry.field
    def carrier_codes(self: pricing.Markup) -> list[str]:
        return self.carrier_codes or []

    @strawberry.field
    def connection_ids(self: pricing.Markup) -> list[str]:
        return self.connection_ids or []

    @strawberry.field
    def organization_ids(self: pricing.Markup) -> list[str]:
        return self.organization_ids or []

    @strawberry.field
    def shipments(
        self: pricing.Markup,
        info: Info,
        filter: inputs.base.ShipmentFilter | None = strawberry.UNSET,
    ) -> utils.Connection[base.ShipmentType] | None:
        _filter = filter if not utils.is_unset(filter) else inputs.base.ShipmentFilter()
        _filter_data = _filter.to_dict()
        _test_mode = getattr(info.context.request, "test_mode", False)

        # Get shipment IDs from Fee table (indexed lookup)
        _fee_filters = dict(markup_id=self.id, test_mode=_test_mode)

        shipment_ids = list(pricing.Fee.objects.filter(**_fee_filters).values_list("shipment_id", flat=True).distinct())

        return utils.paginated_connection(
            filters.ShipmentFilters(
                _filter_data,
                manager.Shipment.objects.filter(id__in=shipment_ids, test_mode=_test_mode),
            ).qs,
            **_filter.pagination(),
        )

    @strawberry.field
    def fees(
        self: pricing.Markup,
        info: Info,
        filter: utils.Paginated | None = strawberry.UNSET,
    ) -> utils.Connection["FeeType"]:
        """Get fees generated by this markup."""
        _filter = filter if not utils.is_unset(filter) else utils.Paginated()
        queryset = pricing.Fee.objects.filter(markup_id=self.id)
        return utils.paginated_connection(queryset, **_filter.pagination())

    @strawberry.field
    def usage(
        self: pricing.Markup,
        info: Info,
        filter: utils.UsageFilter | None = strawberry.UNSET,
    ) -> "ResourceUsageType":
        filter = {
            **(filter.to_dict() if not utils.is_unset(filter) else {}),
            "markup_id": self.id,
        }
        return ResourceUsageType.resolve_usage(info, filter=inputs.ResourceUsageFilter(**filter))

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info, id: str) -> typing.Optional["MarkupType"]:
        return pricing.Markup.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info: Info,
        filter: inputs.MarkupFilter | None = strawberry.UNSET,
    ) -> utils.Connection["MarkupType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.MarkupFilter()
        _filter_data = _filter.to_dict()
        _queryset_filters = {}

        if _filter_data.get("id"):
            _queryset_filters["id"] = _filter_data["id"]
        if _filter_data.get("name"):
            _queryset_filters["name__icontains"] = _filter_data["name"]
        if _filter_data.get("active") is not None:
            _queryset_filters["active"] = _filter_data["active"]
        if _filter_data.get("markup_type"):
            _queryset_filters["markup_type"] = _filter_data["markup_type"]
        if _filter_data.get("account_id"):
            _queryset_filters["organization_ids__contains"] = [_filter_data["account_id"]]
        if _filter_data.get("meta_key"):
            _key = f"meta__{_filter_data['meta_key']}"
            if _filter_data.get("meta_value"):
                _queryset_filters[f"{_key}__icontains"] = _filter_data["meta_value"]
            else:
                _queryset_filters[f"{_key}__isnull"] = False
        if _filter_data.get("metadata_key"):
            _key = f"metadata__{_filter_data['metadata_key']}"
            if _filter_data.get("metadata_value"):
                _queryset_filters[f"{_key}__icontains"] = _filter_data["metadata_value"]
            else:
                _queryset_filters[f"{_key}__isnull"] = False

        queryset = pricing.Markup.objects.filter(**_queryset_filters)
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class FeeType:
    """Admin GraphQL type for Fee model (immutable snapshot)."""

    object_type: str
    id: str
    name: str
    amount: float
    currency: str
    fee_type: str
    percentage: float | None = None
    markup_id: str | None = None
    shipment_id: str
    account_id: str | None = None
    connection_id: str
    carrier_code: str
    service_code: str | None = None
    test_mode: bool = False
    created_at: datetime.datetime

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info, id: str) -> typing.Optional["FeeType"]:
        return pricing.Fee.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info: Info,
        filter: inputs.FeeFilter | None = strawberry.UNSET,
    ) -> utils.Connection["FeeType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.FeeFilter()
        _filter_data = _filter.to_dict()
        _queryset_filters = {}

        if _filter_data.get("markup_id"):
            _queryset_filters["markup_id"] = _filter_data["markup_id"]
        if _filter_data.get("shipment_id"):
            _queryset_filters["shipment_id"] = _filter_data["shipment_id"]
        if _filter_data.get("account_id"):
            _queryset_filters["account_id"] = _filter_data["account_id"]
        if _filter_data.get("carrier_code"):
            _queryset_filters["carrier_code"] = _filter_data["carrier_code"]
        if _filter_data.get("date_after"):
            _queryset_filters["created_at__gte"] = _filter_data["date_after"]
        if _filter_data.get("date_before"):
            _queryset_filters["created_at__lte"] = _filter_data["date_before"]

        queryset = pricing.Fee.objects.filter(**_queryset_filters)
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class AdminSystemUsageType(base.SystemUsageType):
    total_addons_charges: float | None = None
    addons_charges: list[utils.UsageStatType] | None = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info: Info,
        filter: utils.UsageFilter | None = strawberry.UNSET,
    ) -> "AdminSystemUsageType":
        _filter_data = filter.to_dict() if not utils.is_unset(filter) else {}
        base_usage = base.SystemUsageType.resolve(info, filter=utils.UsageFilter(**_filter_data))
        resource_usage = ResourceUsageType.resolve_usage(info, filter=utils.UsageFilter(**_filter_data))

        return AdminSystemUsageType(
            addons_charges=resource_usage.addons_charges,
            order_volume=base_usage.order_volume,
            total_errors=base_usage.total_errors,
            total_requests=base_usage.total_requests,
            total_trackers=base_usage.total_trackers,
            total_shipments=base_usage.total_shipments,
            organization_count=base_usage.organization_count,
            user_count=base_usage.user_count,
            total_shipping_spend=base_usage.total_shipping_spend,
            total_addons_charges=resource_usage.total_addons_charges,
            api_errors=base_usage.api_errors,
            api_requests=base_usage.api_requests,
            order_volumes=base_usage.order_volumes,
            shipment_count=base_usage.shipment_count,
            shipping_spend=base_usage.shipping_spend,
            tracker_count=base_usage.tracker_count,
        )
