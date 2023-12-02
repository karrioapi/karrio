import typing
import strawberry
from constance import config
from django.conf import settings
from strawberry.types import Info
import django.contrib.auth as auth

import karrio.server.admin.utils as admin
import karrio.server.graph.utils as utils
import karrio.server.core.filters as filters
import karrio.server.pricing.models as pricing
import karrio.server.providers.models as providers
import karrio.server.graph.schemas.base.types as base
import karrio.server.admin.schemas.base.inputs as inputs

User = auth.get_user_model()


@strawberry.type
class UserType(base.UserType):
    id: int

    @staticmethod
    @utils.authentication_required
    def me(info) -> "UserType":
        return User.objects.get(id=info.context.request.user.id)

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info,
        email: str = strawberry.UNSET,
    ) -> typing.Optional["UserType"]:
        queryset = User.objects.filter(email=email)

        if settings.MULTI_ORGANIZATIONS:
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
        queryset = filters.UserFilter(_filter.to_dict(), User.objects.filter()).qs

        if settings.MULTI_ORGANIZATIONS:
            queryset = queryset.filter(
                orgs_organization__users__id=info.context.request.user.id
            )

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
class UsageStatType:
    label: typing.Optional[str] = None
    count: typing.Optional[int] = None
    date: typing.Optional[str] = None

    @staticmethod
    def parse(value: dict):
        return UsageStatType(
            **{k: v for k, v in value.items() if k in UsageStatType.__annotations__}
        )


@strawberry.type
class SystemUsageType:
    total_errors: typing.Optional[int] = None
    total_orders: typing.Optional[int] = None
    total_requests: typing.Optional[int] = None
    total_trackers: typing.Optional[int] = None
    total_shipments: typing.Optional[int] = None
    api_errors: typing.List[UsageStatType] = None
    api_requests: typing.List[UsageStatType] = None
    order_volumes: typing.List[UsageStatType] = None
    tracker_volumes: typing.List[UsageStatType] = None
    shipment_volumes: typing.List[UsageStatType] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info,
        filter: typing.Optional[inputs.UsageFilter] = strawberry.UNSET,
    ) -> "SurchargeType":
        api_errors = []
        api_requests = []
        order_volumes = []
        tracker_volumes = []
        shipment_volumes = []

        total_errors = 0
        total_orders = 0
        total_requests = 0
        total_trackers = 0
        total_shipments = 0

        return SystemUsageType(
            total_errors=total_errors,
            total_orders=total_orders,
            total_requests=total_requests,
            total_trackers=total_trackers,
            total_shipments=total_shipments,
            api_errors=[UsageStatType.parse(item) for item in api_errors],
            api_requests=[UsageStatType.parse(item) for item in api_requests],
            order_volumes=[UsageStatType.parse(item) for item in order_volumes],
            tracker_volumes=[UsageStatType.parse(item) for item in tracker_volumes],
            shipment_volumes=[UsageStatType.parse(item) for item in shipment_volumes],
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
    def resolve_list(info) -> typing.List["SurchargeType"]:
        return pricing.Surcharge.objects.filter()


@strawberry.type
class _InstanceConfigType:
    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info) -> "InstanceConfigType":
        return InstanceConfigType(  # type: ignore
            **{k: getattr(config, k) for k in settings.CONSTANCE_CONFIG.keys()}
        )


InstanceConfigType = strawberry.type(
    type(
        "InstanceConfigType",
        (_InstanceConfigType,),
        {
            **{k: strawberry.UNSET for k, _ in settings.CONSTANCE_CONFIG.items()},
            "__annotations__": {
                k: typing.Optional[_def[2]]
                for k, _def in settings.CONSTANCE_CONFIG.items()
            },
        },
    )
)
