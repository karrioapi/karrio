import typing
import datetime
import strawberry
from constance import config
from strawberry.types import Info

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.iam.models as iam
import karrio.server.orgs.models as orgs
import karrio.server.graph.utils as utils
import karrio.server.admin.utils as admin
import karrio.server.core.filters as filters
import karrio.server.pricing.models as pricing
import karrio.server.manager.models as manager
import karrio.server.orgs.filters as org_filters
import karrio.server.providers.models as providers
import karrio.server.orders.models as orders_models
import karrio.server.graph.schemas.base.types as base
import karrio.server.admin.schemas.base.inputs as inputs
import karrio.server.graph.schemas.orders.types as orders_types
import karrio.server.graph.schemas.orgs.types as org_types
import karrio.server.graph.schemas.orgs.inputs as org_inputs


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
    def permissions(self: iam.User, info) -> typing.Optional[typing.List[str]]:
        return self.permissions

    @staticmethod
    @utils.authentication_required
    def me(info) -> "SystemUserType":
        return iam.User.objects.get(id=info.context.request.user.id)

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info,
        email: str = strawberry.UNSET,
    ) -> typing.Optional["SystemUserType"]:
        queryset = iam.User.objects.filter(email=email, is_staff=True)
        return queryset.first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.UserFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemUserType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.UserFilter()
        queryset = filters.UserFilter(_filter.to_dict(), iam.User.objects.filter(is_staff=True)).qs

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
class AccountUsageType(org_types.OrgUsageType):
    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info,
        filter: org_inputs.OrgUsageFilter = strawberry.UNSET,
    ) -> "AccountUsageType":
        _filter = filter.to_dict() if not utils.is_unset(filter) else {}

        org = orgs.Organization.objects.get(id=_filter.pop("id"))
        usage = org_types.OrgUsageType.resolve_usage(
            info, org, filter=org_inputs.OrgUsageFilter(**_filter)
        )

        return AccountUsageType(**usage)


@strawberry.type
class OrganizationAccountType:
    id: str
    name: str
    slug: str
    is_active: bool
    created: datetime.datetime
    modified: datetime.datetime

    @strawberry.field
    def members(self: orgs.Organization) -> typing.List[org_types.OrganizationMemberType]:
        users = [
            org_types.OrganizationMemberType(  # type: ignore
                email=user.email,
                full_name=user.full_name,
                last_login=user.last_login,
                is_owner=self.is_owner(user),
                roles=self.organization_users.get(user=user).roles,
                is_admin=self.organization_users.get(user=user).is_admin,
                user_id=str(user.id),
            )
            for user in self.users.filter(is_active=True)
        ]
        invites = [
            org_types.OrganizationMemberType(  # type: ignore
                email=getattr(invite.invitee, "email", invite.invitee_identifier),
                full_name=getattr(invite.invitee, "full_name", ""),
                is_admin=False,
                is_owner=False,
                invitation=invite,
                roles=[orgs.OrganizationUserRole.member],
                user_id=str(invite.invitee.id) if invite.invitee else None,
            )
            for invite in self.organization_invites.all()
        ]

        return users + invites


    @strawberry.field
    def usage(
        self: orgs.Organization,
        info: Info,
        filter: typing.Optional[org_inputs.OrgUsageFilter] = strawberry.UNSET,
    ) -> AccountUsageType:
        _filter = {
            "id": self.id,
            **(filter.to_dict() if not utils.is_unset(filter) else {}),
        }
        return AccountUsageType.resolve(
            info, filter=org_inputs.OrgUsageFilter(**_filter)
        )

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info, id: typing.Optional[str] = strawberry.UNSET
    ) -> typing.Optional["OrganizationAccountType"]:
        return orgs.Organization.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AccountFilter] = strawberry.UNSET,
    ) -> utils.Connection["OrganizationAccountType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.AccountFilter()
        queryset = org_filters.OrgFilters(
            _filter.to_dict(), orgs.Organization.objects.filter()
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class AccountCarrierConnectionType(base.SystemConnectionType):

    @strawberry.field
    def account_id(self: providers.Carrier) -> typing.Optional[str]:
        return getattr(self.org.first(), "id", None)

    @strawberry.field
    def account(self: providers.Carrier) -> typing.Optional[OrganizationAccountType]:
        return self.org.first()

    @strawberry.field
    def usage(
        self: providers.Carrier,
        info: Info,
        filter: typing.Optional[utils.UsageFilter] = strawberry.UNSET,
    ) -> "ResourceUsageType":
        # Create a new filter with carrier_connection_id added
        base_filter = filter.to_dict() if not utils.is_unset(filter) else {}
        enhanced_filter = utils.UsageFilter(
            date_after=base_filter.get('date_after'),
            date_before=base_filter.get('date_before'),
            omit=base_filter.get('omit')
        )

        # Create a custom filter dict that includes carrier_connection_id for internal usage
        import types as python_types

        # Add carrier_connection_id to the filter for internal processing
        enhanced_filter_dict = enhanced_filter.to_dict()
        enhanced_filter_dict["carrier_connection_id"] = self.id

        # Create a mock filter object that includes the carrier_connection_id
        mock_filter = python_types.SimpleNamespace(**enhanced_filter_dict)
        mock_filter.to_dict = lambda: enhanced_filter_dict

        return ResourceUsageType.resolve_usage(info, filter=mock_filter)

    @strawberry.field
    def shipments(
        self: providers.Carrier,
        info: Info,
        filter: typing.Optional[inputs.SystemShipmentFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemShipmentType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.SystemShipmentFilter()
        _filter_data = _filter.to_dict()
        queryset = filters.ShipmentFilters(_filter_data, self.related_shipments.filter()).qs

        return utils.paginated_connection(queryset, **_filter.pagination())

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info, id: str) -> typing.Optional["AccountCarrierConnectionType"]:
        _test_mode = getattr(info.context.request, "test_mode", False)
        return providers.Carrier.user_carriers.filter(id=id, test_mode=_test_mode).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AccountCarrierConnectionFilter] = strawberry.UNSET,
    ) -> typing.List["AccountCarrierConnectionType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.AccountCarrierConnectionFilter()
        _filter_data = _filter.to_dict()
        _test_mode = getattr(info.context.request, "test_mode", False)
        _org_id = lib.identity(
            dict(org__id=_filter_data.get("account_id"))
            if _filter_data.get("account_id")
            else {}
        )

        queryset = filters.CarrierFilters(
            _filter_data,
            providers.Carrier.user_carriers.filter(test_mode=_test_mode, **_org_id)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class SystemCarrierConnectionType(base.CarrierConnectionType):
    object_type: typing.Optional[str]

    @strawberry.field
    def usage(
        self: providers.Carrier,
        info: Info,
        filter: typing.Optional[utils.UsageFilter] = strawberry.UNSET,
    ) -> "ResourceUsageType":
        # Create a new filter with carrier_connection_id added
        base_filter = filter.to_dict() if not utils.is_unset(filter) else {}
        enhanced_filter = utils.UsageFilter(
            date_after=base_filter.get('date_after'),
            date_before=base_filter.get('date_before'),
            omit=base_filter.get('omit')
        )

        # Create a custom filter dict that includes carrier_connection_id for internal usage
        import types as python_types

        # Add carrier_connection_id to the filter for internal processing
        enhanced_filter_dict = enhanced_filter.to_dict()
        enhanced_filter_dict["carrier_connection_id"] = self.id

        # Create a mock filter object that includes the carrier_connection_id
        mock_filter = python_types.SimpleNamespace(**enhanced_filter_dict)
        mock_filter.to_dict = lambda: enhanced_filter_dict

        return ResourceUsageType.resolve_usage(info, filter=mock_filter)

    @strawberry.field
    def shipments(
        self: providers.Carrier,
        info: Info,
        filter: typing.Optional[inputs.SystemShipmentFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemShipmentType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.SystemShipmentFilter()
        _filter_data = _filter.to_dict()
        queryset = filters.ShipmentFilters(_filter_data, self.shipments.filter()).qs

        return utils.paginated_connection(queryset, **_filter.pagination())

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info, id: str) -> typing.Optional["SystemCarrierConnectionType"]:
        connection = providers.Carrier.system_carriers.filter(
            id=id,
            test_mode=getattr(info.context.request, "test_mode", False),
        )

        return connection.first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.base.CarrierFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemCarrierConnectionType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.base.CarrierFilter()
        queryset = filters.CarrierFilters(
            _filter.to_dict(),
            providers.Carrier.system_carriers.filter(
                test_mode=getattr(info.context.request, "test_mode", False),
            ),
        ).qs

        return utils.paginated_connection(queryset)


def _bulk_load_constance_config(keys):
    """Bulk load constance configuration values to avoid N+1 queries."""
    from django.db import connection
    from constance.backends.database.models import Constance
    
    # Use Django ORM to bulk fetch all values in a single query
    constance_values = Constance.objects.filter(key__in=keys).values('key', 'value')
    values_dict = {item['key']: item['value'] for item in constance_values}
    
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
class _InstanceConfigType:
    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info: Info) -> "InstanceConfigType":
        if conf.settings.tenant:
            return InstanceConfigType(  # type: ignore
                **{
                    k: getattr(conf.settings, k, None)
                    for k in conf.settings.CONSTANCE_CONFIG.keys()
                    if k not in PRIVATE_CONFIGS
                },
                **{
                    k: conf.settings.tenant.feature_flags.get(k, None)
                    for k in PRIVATE_CONFIGS
                },
            )

        # Use bulk loading to avoid N+1 queries
        all_keys = list(conf.settings.CONSTANCE_CONFIG.keys())
        bulk_values = _bulk_load_constance_config(all_keys)
        
        return InstanceConfigType(  # type: ignore
            **bulk_values
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
        _test_mode = getattr(info.context.request, "test_mode", False)
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


@strawberry.type
class ResourceUsageType:
    total_trackers: typing.Optional[int] = None
    total_shipments: typing.Optional[int] = None
    total_addons_charges: typing.Optional[float] = None
    total_shipping_spend: typing.Optional[float] = None
    addons_charges: typing.Optional[typing.List[utils.UsageStatType]] = None
    shipping_spend: typing.Optional[typing.List[utils.UsageStatType]] = None
    tracker_count: typing.Optional[typing.List[utils.UsageStatType]] = None

    @staticmethod
    def resolve_usage(
        info,
        filter: utils.UsageFilter = strawberry.UNSET,
    ) -> "ResourceUsageType":
        import django.db.models as models
        import django.db.models.functions as functions
        import karrio.server.manager.models as manager

        _test_mode = info.context.request.test_mode
        _test_filter = dict(test_mode=_test_mode)
        _filter = {
            "date_before": datetime.datetime.now(),
            "date_after": (datetime.datetime.now() - datetime.timedelta(days=30)),
            **filter.to_dict(),
        }
        _surcharge_id = _filter.get("surcharge_id")
        _surcharge_filter = lib.identity(
            dict(selected_rate__extra_charges__icontains=_surcharge_id)
            if _surcharge_id
            else {}
        )
        _account_filter = lib.identity(
            dict(org__id=_filter.get("account_id"))
            if _filter.get("account_id")
            else {}
        )
        _connection_filter = lib.identity(
            dict(selected_rate__meta__carrier_connection_id=_filter.get("carrier_connection_id"))
            if _filter.get("carrier_connection_id")
            else {}
        )
        _tracker_filter = lib.identity(
            dict(tracking_carrier_id=_filter.get("carrier_connection_id"))
            if _filter.get("carrier_connection_id")
            else {}
        )

        surcharges = lib.identity(
            pricing.Surcharge.objects.filter(id=_surcharge_id)
            if _surcharge_id else pricing.Surcharge.objects.all()
        )
        shipments = lib.identity(
            filters.ShipmentFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                    status__not_in=["draft", "cancelled"],
                ),
                manager.Shipment.objects
                .filter(**{
                    **_test_filter,
                    **_surcharge_filter,
                    **_connection_filter,
                    **_account_filter,
                })
            )
        )

        shipping_spend = lib.identity(
            shipments
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(
                count=models.Count("id"),
                amount=functions.Coalesce(
                    models.Sum(
                        functions.Cast("selected_rate__total_charge", models.FloatField())
                    ),
                    models.Value(0.0)
                ),
            )
            .order_by("-date")
        )
        addons_charges = lib.identity([
            {
                "date": date,
                "count": len([s for s in group if any(surcharges.filter(id=c.get("id")).exists() for c in (s.selected_rate or {}).get("extra_charges", []))]),
                "amount": sum(
                    sum(float(c.get("amount", 0)) for c in (s.selected_rate or {}).get("extra_charges", []) if surcharges.filter(id=c.get("id")).exists())
                    for s in group
                ),
            }
            for date, group in {
                date: [s for s in shipments.qs if s.created_at.date() == date]
                for date in {s.created_at.date() for s in shipments.qs}
            }.items()
        ])
        tracker_count = (
            filters.TrackerFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                ),
                manager.Tracking.objects.filter(**{
                    **_test_filter,
                    **_tracker_filter,
                    **_account_filter,
                }),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(count=models.Count("id"))
            .order_by("-date")
        )

        total_shipments = shipments.qs.count()
        total_shipping_spend = lib.to_decimal(
            sum([item["amount"] for item in shipping_spend if item["amount"] is not None], 0.0)
        )
        total_addons_charges = lib.to_decimal(
            sum([item["amount"] for item in addons_charges if item["amount"] is not None], 0.0)
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
class SystemShipmentType(base.ShipmentType):
    """System-specific shipment type with account context and non-private data"""

    @strawberry.field
    def account_id(self: manager.Shipment) -> typing.Optional[str]:
        return getattr(self.org.first(), "id", None)

    @strawberry.field
    def account(self: manager.Shipment) -> typing.Optional[OrganizationAccountType]:
        return self.org.first()

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["SystemShipmentType"]:
        _test_mode = getattr(info.context.request, "test_mode", False)
        return manager.Shipment.objects.filter(id=id, test_mode=_test_mode).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.SystemShipmentFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemShipmentType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.SystemShipmentFilter()
        _filter_data = _filter.to_dict()
        _org_id = lib.identity(
            dict(org__id=_filter_data.get("account_id"))
            if _filter_data.get("account_id")
            else {}
        )
        _test_mode = dict(test_mode=getattr(info.context.request, "test_mode", False))

        queryset = filters.ShipmentFilters(
            _filter_data, manager.Shipment.objects.filter(**{ **_test_mode, **_org_id })
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class SystemTrackerType(base.TrackerType):
    """Admin-specific tracker type with account context and non-private data"""

    @strawberry.field
    def account_id(self: manager.Tracking) -> typing.Optional[str]:
        return getattr(self.org.first(), "id", None)

    @strawberry.field
    def account(self: manager.Tracking) -> typing.Optional[OrganizationAccountType]:
        return self.org.first()

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["SystemTrackerType"]:
        _test_mode = getattr(info.context.request, "test_mode", False)
        return manager.Tracking.objects.filter(id=id, test_mode=_test_mode).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.SystemTrackerFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemTrackerType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.SystemTrackerFilter()
        _filter_data = _filter.to_dict()
        _org_id = lib.identity(
            dict(org__id=_filter_data.get("account_id"))
            if _filter_data.get("account_id")
            else {}
        )
        _test_mode = dict(test_mode=getattr(info.context.request, "test_mode", False))

        queryset = filters.TrackerFilters(
            _filter_data, manager.Tracking.objects.filter(**{ **_test_mode, **_org_id })
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class SystemOrderType(orders_types.OrderType):
    """Admin-specific order type with account context and non-private data"""

    @strawberry.field
    def account_id(self: orders_models.Order) -> typing.Optional[str]:
        return getattr(self.org.first(), "id", None)

    @strawberry.field
    def account(self: orders_models.Order) -> typing.Optional[OrganizationAccountType]:
        return self.org.first()

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["SystemOrderType"]:
        _test_mode = getattr(info.context.request, "test_mode", False)
        return orders_models.Order.objects.filter(id=id, test_mode=_test_mode).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.SystemOrderFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemOrderType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.SystemOrderFilter()
        _filter_data = _filter.to_dict()
        _org_id = lib.identity(
            dict(org__id=_filter_data.get("account_id"))
            if _filter_data.get("account_id")
            else {}
        )
        _test_mode = dict(test_mode=getattr(info.context.request, "test_mode", False))

        queryset = filters.OrderFilters(
            _filter_data,
            orders_models.Order.objects.filter(**{ **_test_mode, **_org_id })
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class AddonType:
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
    def carrier_accounts(self: pricing.Surcharge) -> typing.List[AccountCarrierConnectionType]:
        return self.carrier_accounts.all()

    @strawberry.field
    def shipments(self: pricing.Surcharge, info: Info, filter: typing.Optional[inputs.SystemShipmentFilter] = strawberry.UNSET) -> typing.Optional[utils.Connection["SystemShipmentType"]]:
        _filter = filter if not utils.is_unset(filter) else inputs.SystemShipmentFilter()
        _filter_data = _filter.to_dict()
        _test_mode = dict(test_mode=getattr(info.context.request, "test_mode", False))
        _surcharge_filter = dict(selected_rate__extra_charges__id=self.id)
        _org_id = lib.identity(
            dict(org__id=_filter_data.pop("account_id"))
            if _filter_data.get("account_id")
            else {}
        )

        return utils.paginated_connection(
            filters.ShipmentFilters(
                _filter_data,
                manager.Shipment.objects.filter(**{ **_test_mode, **_org_id, **_surcharge_filter }),
            ).qs,
            **_filter.pagination()
        )

    @strawberry.field
    def usage(
        self: pricing.Surcharge,
        info: Info,
        filter: typing.Optional[utils.UsageFilter] = strawberry.UNSET,
    ) -> "ResourceUsageType":
        filter = {
            **(filter.to_dict() if not utils.is_unset(filter) else {}),
            "surcharge_id": self.id,
        }
        return ResourceUsageType.resolve_usage(info, filter=utils.UsageFilter(**filter))

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(info, id: str) -> typing.Optional["AddonType"]:
        return pricing.Surcharge.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AddonFilter] = strawberry.UNSET,
    ) -> utils.Connection["AddonType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.AddonFilter()
        queryset = pricing.Surcharge.objects.filter()
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class AdminSystemUsageType(base.SystemUsageType):
    total_addons_charges: typing.Optional[float] = None
    addons_charges: typing.Optional[typing.List[utils.UsageStatType]] = None

    @staticmethod
    @utils.authentication_required
    @admin.staff_required
    def resolve(
        info: Info,
        filter: typing.Optional[utils.UsageFilter] = strawberry.UNSET,
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
