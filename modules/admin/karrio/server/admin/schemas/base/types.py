import typing
import datetime
import strawberry
from constance import config
from strawberry.types import Info
import django.db.models as models
import django.db.models.functions as functions

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.iam.models as iam
import karrio.server.core.models as core
import karrio.server.admin.utils as admin
import karrio.server.graph.utils as utils
import karrio.server.core.filters as filters
import karrio.server.orders.models as orders
import karrio.server.pricing.models as pricing
import karrio.server.manager.models as manager
import karrio.server.orders.filters as order_filters
import karrio.server.providers.models as providers
import karrio.server.graph.schemas.base.types as base
import karrio.server.admin.schemas.base.inputs as inputs


@strawberry.type
class UserType(base.UserType):
    id: int

    @strawberry.field
    def permissions(self: iam.User, info) -> typing.Optional[typing.List[str]]:
        return self.permissions

    @staticmethod
    @utils.authentication_required
    def me(info) -> "UserType":
        return iam.User.objects.get(id=info.context.request.user.id)

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info,
        email: str = strawberry.UNSET,
    ) -> typing.Optional["UserType"]:
        queryset = iam.User.objects.filter(email=email)

        if conf.settings.MULTI_ORGANIZATIONS:
            return queryset.filter(
                orgs_organization__users__id=info.context.request.user.id
            ).first()

        return queryset.first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.UserFilter] = strawberry.UNSET,
    ) -> utils.Connection["UserType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.UserFilter()
        queryset = filters.UserFilter(_filter.to_dict(), iam.User.objects.filter()).qs

        if conf.settings.MULTI_ORGANIZATIONS:
            queryset = queryset.filter(
                orgs_organization__users__id=info.context.request.user.id
            ).distinct()

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class PermissionGroupType:
    id: int
    name: str

    @strawberry.field
    def permissions(self: iam.Group) -> typing.Optional[typing.List[str]]:
        return self.permissions.all().values_list("name", flat=True)

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.PermissionGroupFilter] = strawberry.UNSET,
    ) -> utils.Connection["PermissionGroupType"]:
        _filter = (
            filter if not utils.is_unset(filter) else inputs.PermissionGroupFilter()
        )
        queryset = iam.Group.objects.filter()

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class CarrierConnectionType(base.SystemConnectionType):
    id: str

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.base.ShipmentFilter] = strawberry.UNSET,
    ) -> typing.List["CarrierConnectionType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.ShipmentFilter()
        query = providers.Carrier.user_carrier.filter(
            test_mode=getattr(info.context.request, "test_mode", False),
        )
        queryset = filters.ShipmentFilters(_filter.to_dict(), query).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.interface
class SystemConnectionType:
    object_type: typing.Optional[str]

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info, id: str) -> typing.Optional["SystemCarrierConnectionType"]:
        connection = providers.Carrier.system_carriers.filter(
            id=id,
            test_mode=getattr(info.context.request, "test_mode", False),
        )

        return (
            base.ConnectionType.parse(connection.first(), SystemCarrierSettings)
            if connection.exists()
            else None
        )

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(info) -> typing.List["SystemCarrierConnectionType"]:
        connections = providers.Carrier.system_carriers.filter(
            test_mode=getattr(info.context.request, "test_mode", False),
        )

        return [
            base.ConnectionType.parse(_, SystemCarrierSettings) for _ in connections
        ]


SystemCarrierSettings = {
    name: strawberry.type(
        type(
            settings.__name__,
            (
                settings,
                SystemConnectionType,
            ),
            {
                "object_type": strawberry.UNSET,
                "__annotations__": {"object_type": typing.Optional[str]},
            },
        )
    )
    for name, settings in base.CarrierSettings.items()
}
SystemCarrierConnectionType: typing.Any = strawberry.union(
    "SystemCarrierConnectionType", types=(*(T for T in SystemCarrierSettings.values()),)
)


@strawberry.type
class SystemUsageType:
    total_errors: typing.Optional[int] = None
    order_volume: typing.Optional[float] = None
    total_requests: typing.Optional[int] = None
    total_trackers: typing.Optional[int] = None
    total_shipments: typing.Optional[int] = None
    organization_count: typing.Optional[int] = None
    total_shipping_spend: typing.Optional[float] = None
    api_errors: typing.Optional[typing.List[utils.UsageStatType]] = None
    api_requests: typing.Optional[typing.List[utils.UsageStatType]] = None
    order_volumes: typing.Optional[typing.List[utils.UsageStatType]] = None
    shipment_count: typing.Optional[typing.List[utils.UsageStatType]] = None
    shipping_spend: typing.Optional[typing.List[utils.UsageStatType]] = None
    tracker_count: typing.Optional[typing.List[utils.UsageStatType]] = None

    @staticmethod
    @utils.authentication_required
    def resolve(
        info,
        filter: typing.Optional[utils.UsageFilter] = strawberry.UNSET,
    ) -> "SystemUsageType":
        _test_mode = info.context.request.test_mode
        _test_filter = dict(test_mode=_test_mode)
        _filter = {
            "date_before": datetime.datetime.now(),
            "date_after": (datetime.datetime.now() - datetime.timedelta(days=30)),
            **(filter if not utils.is_unset(filter) else utils.UsageFilter()).to_dict(),
        }

        api_requests = (
            filters.LogFilter(
                _filter,
                core.APILogIndex.objects.filter(**_test_filter),
            )
            .qs.annotate(date=functions.TruncDay("requested_at"))
            .values("date")
            .annotate(count=models.Count("id"))
            .order_by("-date")
        )
        api_errors = (
            filters.LogFilter(
                {**_filter, "status": "failed"},
                core.APILogIndex.objects.filter(**_test_filter),
            )
            .qs.annotate(date=functions.TruncDay("requested_at"))
            .values("date")
            .annotate(count=models.Count("id"))
            .order_by("-date")
        )
        order_volumes = (
            order_filters.OrderFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                ),
                orders.Order.objects.filter(**_test_filter).exclude(
                    status__in=["cancelled", "unfulfilled"]
                ),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(
                count=models.Sum(
                    models.F("line_items__value_amount")
                    * models.F("line_items__quantity")
                )
            )
            .order_by("-date")
        )
        shipment_count = (
            filters.ShipmentFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                ),
                manager.Shipment.objects.filter(**_test_filter),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(count=models.Count("id"))
            .order_by("-date")
        )
        shipping_spend = (
            filters.ShipmentFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                ),
                manager.Shipment.objects.filter(**_test_filter).exclude(
                    status__in=["cancelled", "draft"]
                ),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(
                count=models.Sum(
                    functions.Cast("selected_rate__total_charge", models.FloatField())
                )
            )
            .order_by("-date")
        )
        tracker_count = (
            filters.TrackerFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                ),
                manager.Tracking.objects.filter(**_test_filter),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(count=models.Count("id"))
            .order_by("-date")
        )

        total_errors = sum([item["count"] for item in api_errors], 0)
        total_requests = sum([item["count"] for item in api_requests], 0)
        total_trackers = sum([item["count"] for item in tracker_count], 0)
        total_shipments = sum([item["count"] for item in shipment_count], 0)
        order_volume = lib.to_money(sum([item["count"] for item in order_volumes], 0.0))
        total_shipping_spend = lib.to_money(
            sum([item["count"] for item in shipping_spend], 0.0)
        )
        organization_count = 0

        if conf.settings.MULTI_ORGANIZATIONS:
            import karrio.server.orgs.models as orgs

            organization_count = orgs.Organization.objects.count()

        return SystemUsageType(
            order_volume=order_volume,
            total_errors=total_errors,
            total_requests=total_requests,
            total_trackers=total_trackers,
            total_shipments=total_shipments,
            organization_count=organization_count,
            total_shipping_spend=total_shipping_spend,
            api_errors=[utils.UsageStatType.parse(item) for item in api_errors],
            api_requests=[utils.UsageStatType.parse(item) for item in api_requests],
            order_volumes=[utils.UsageStatType.parse(item) for item in order_volumes],
            shipment_count=[utils.UsageStatType.parse(item) for item in shipment_count],
            shipping_spend=[utils.UsageStatType.parse(item) for item in shipping_spend],
            tracker_count=[utils.UsageStatType.parse(item) for item in tracker_count],
        )


@strawberry.type
class SurchargeType:
    object_type: str
    id: str
    name: str
    active: bool
    amount: float
    surcharge_type: str

    @strawberry.field
    def services(self: pricing.Surcharge) -> typing.List[str]:
        return self.services or []

    @strawberry.field
    def carriers(self: pricing.Surcharge) -> typing.List[str]:
        return self.carriers or []

    @strawberry.field
    def carrier_accounts(self: pricing.Surcharge) -> typing.List[CarrierConnectionType]:
        return [
            base.ConnectionType.parse(c, SystemCarrierSettings)
            for c in self.carrier_accounts.all()
        ]

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info, id: str) -> typing.Optional["SurchargeType"]:
        return pricing.Surcharge.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.SurchargeFilter] = strawberry.UNSET,
    ) -> typing.List["SurchargeType"]:
        return pricing.Surcharge.objects.filter()


@strawberry.type
class _InstanceConfigType:
    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info) -> "InstanceConfigType":
        return InstanceConfigType(  # type: ignore
            **{k: getattr(config, k) for k in conf.settings.CONSTANCE_CONFIG.keys()}
        )


InstanceConfigType = strawberry.type(
    type(
        "InstanceConfigType",
        (_InstanceConfigType,),
        {
            **{k: strawberry.UNSET for k, _ in conf.settings.CONSTANCE_CONFIG.items()},
            "__annotations__": {
                k: typing.Optional[_def[2]]
                for k, _def in conf.settings.CONSTANCE_CONFIG.items()
            },
        },
    )
)


@strawberry.type
class SystemRateSheetType(base.RateSheetType):
    id: str

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info,
        id: str,
    ) -> typing.Optional["SystemRateSheetType"]:
        return providers.RateSheet.objects.filter(id=id, is_system=True).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.base.RateSheetFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemRateSheetType"]:
        _filter = (
            filter if not utils.is_unset(filter) else inputs.base.RateSheetFilter()
        )
        queryset = filters.RateSheetFilter(
            _filter.to_dict(), providers.RateSheet.objects.filter(is_system=True)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())
