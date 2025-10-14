import typing
import datetime
import strawberry
from strawberry.types import Info

import karrio.lib as lib
import karrio.server.orgs.utils as orgs
import karrio.server.graph.utils as utils
import karrio.server.orgs.models as models
import karrio.server.core.filters as filters
import karrio.server.serializers as serializers
import karrio.server.graph.schemas.base as base
import karrio.server.orders.filters as order_filters
import karrio.server.graph.schemas.orgs.inputs as inputs
import karrio.server.user.serializers as user_serializers


@strawberry.type
class OrganizationUserType:
    email: str
    is_admin: bool
    is_owner: bool
    is_staff: typing.Optional[bool] = None
    full_name: typing.Optional[str] = None
    last_login: typing.Optional[datetime.datetime] = None
    date_joined: typing.Optional[datetime.datetime] = None
    roles: typing.Optional[typing.List[orgs.OrganizationUserRole]] = None
    user_id: typing.Optional[str] = None


@strawberry.type
class OrganizationInvitationType:
    object_type: str
    id: str
    guid: str
    invitee_identifier: str
    created: datetime.datetime
    modified: datetime.datetime
    invited_by: base.types.UserType
    invitee: typing.Optional[base.types.UserType] = None

    @strawberry.field
    def organization_name(self: models.Organization) -> str:
        return self.organization.name

    @staticmethod
    def resolve(
        info,
        id: typing.Optional[str] = strawberry.UNSET,
        guid: typing.Optional[str] = strawberry.UNSET,
    ) -> typing.Optional["OrganizationInvitationType"]:
        _filter = lib.to_dict(
            dict(
                id=(id if id is not strawberry.UNSET else None),
                guid=(guid if guid is not strawberry.UNSET else None),
            )
        )

        return models.OrganizationInvitation.objects.filter(**_filter).first()


@strawberry.type
class OrganizationMemberType:
    email: str
    is_admin: bool
    roles: typing.List[orgs.OrganizationUserRole]
    is_owner: typing.Optional[bool] = None
    full_name: typing.Optional[str] = None
    last_login: typing.Optional[datetime.datetime] = None
    invitation: typing.Optional[OrganizationInvitationType] = None
    roles: typing.Optional[typing.List[orgs.OrganizationUserRole]] = None
    user_id: typing.Optional[str] = None


@strawberry.type
class OrganizationType:
    id: str
    name: str
    slug: str
    is_active: bool
    created: datetime.datetime
    modified: datetime.datetime
    metadata: typing.Optional[utils.JSON] = None

    @strawberry.field
    def current_user(self: models.Organization, info: Info) -> OrganizationMemberType:
        import django.forms.models as models

        user = info.context.request.user
        return lib.to_object(
            OrganizationUserType,  # type: ignore
            {
                **{
                    k: v
                    for k, v in models.model_to_dict(user).items()
                    if k in OrganizationUserType.__annotations__.keys()
                },
                "is_admin": self.organization_users.get(user=user).is_admin,
                "is_owner": self.is_owner(user),
                "roles": self.organization_users.get(user=user).roles,
                "user_id": str(user.id),
            },
        )

    @strawberry.field
    def members(self: models.Organization) -> typing.List[OrganizationMemberType]:
        users = [
            OrganizationMemberType(  # type: ignore
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
            OrganizationMemberType(  # type: ignore
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
    def organization_invites(
        self: models.Organization,
    ) -> typing.List[OrganizationInvitationType]:
        return self.organization_invites.all()

    @strawberry.field
    def token(self: models.Organization, info: Info) -> str:
        context = serializers.Context(
            org=self,
            user=info.context.request.user,
            test_mode=info.context.request.test_mode,
        )

        return user_serializers.TokenSerializer.retrieve_token(context, org_id=self.id)

    @strawberry.field
    def workspace_config(
        self: models.Organization,
    ) -> typing.Optional[base.types.WorkspaceConfigType]:
        return self.config

    @strawberry.field
    def usage(
        self: models.Organization,
        info: Info,
        filter: typing.Optional[utils.UsageFilter] = strawberry.UNSET,
    ) -> "OrgUsageType":
        filter = {
            "id": self.id,
            **(filter.to_dict() if not utils.is_unset(filter) else {}),
        }
        return OrgUsageType.resolve(info, filter=inputs.OrgUsageFilter(**filter))

    @staticmethod
    @utils.authentication_required
    def resolve(
        info, id: typing.Optional[str] = strawberry.UNSET
    ) -> typing.Optional["OrganizationType"]:
        if id != strawberry.UNSET:
            return models.Organization.objects.get(
                id=id,
                users__id=info.context.request.user.id,
                is_active=True,
            )

        return info.context.request.org

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info: Info,
        filter: typing.Optional[inputs.OrgFilter] = strawberry.UNSET,
    ) -> utils.Connection["OrganizationType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.OrgFilter()
        queryset = models.Organization.objects.filter(
            users__id=info.context.request.user.id,
            is_active=True,
        )

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class OrgUsageType:
    members: typing.Optional[int] = None
    total_errors: typing.Optional[int] = None
    order_volume: typing.Optional[float] = None
    total_requests: typing.Optional[int] = None
    total_trackers: typing.Optional[int] = None
    total_shipments: typing.Optional[int] = None
    unfulfilled_orders: typing.Optional[int] = None
    total_shipping_spend: typing.Optional[float] = None
    total_addons_charges: typing.Optional[float] = None
    api_errors: typing.Optional[typing.List[utils.UsageStatType]] = None
    api_requests: typing.Optional[typing.List[utils.UsageStatType]] = None
    order_volumes: typing.Optional[typing.List[utils.UsageStatType]] = None
    shipment_count: typing.Optional[typing.List[utils.UsageStatType]] = None
    shipping_spend: typing.Optional[typing.List[utils.UsageStatType]] = None
    tracker_count: typing.Optional[typing.List[utils.UsageStatType]] = None

    @staticmethod
    def resolve_usage(
        info,
        org: models.Organization,
        filter: utils.UsageFilter = strawberry.UNSET,
    ) -> "OrgUsageType":
        import django.db.models as models
        import django.db.models.functions as functions

        _test_mode = info.context.request.test_mode
        _test_filter = dict(test_mode=_test_mode)
        _filter = {
            "date_before": datetime.datetime.now(),
            "date_after": (datetime.datetime.now() - datetime.timedelta(days=30)),
            **(filter.to_dict() if not utils.is_unset(filter) else {}),
        }

        api_requests = (
            filters.LogFilter(
                _filter, org.logs.filter(apilogindex__test_mode=_test_mode)
            )
            .qs.annotate(date=functions.TruncDay("requested_at"))
            .values("date")
            .annotate(count=models.Count("id"))
            .order_by("-date")
        )
        api_errors = (
            filters.LogFilter(
                {**_filter, "status": "failed"},
                org.logs.filter(apilogindex__test_mode=_test_mode),
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
                org.orders.filter(**_test_filter),
            )
            .qs.exclude(status__in=["cancelled", "unfulfilled"])
            .annotate(date=functions.TruncDay("created_at"))
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
                org.shipments.filter(**_test_filter),
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
                org.shipments.filter(**_test_filter),
            )
            .qs.exclude(status__in=["cancelled", "draft"])
            .annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(
                count=models.Sum(
                    functions.Cast(
                        "selected_rate__total_charge",
                        models.FloatField(),
                    ),
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
                org.trackers.filter(**_test_filter),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(count=models.Count("id"))
            .order_by("-date")
        )
        addons_charges = (
            filters.ShipmentFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                    status__not_in=["draft", "cancelled"],
                ),
                org.shipments.filter(**_test_filter).exclude(
                    models.Q(selected_rate__meta__surcharge_amount__isnull=True)
                    | models.Q(selected_rate__meta__surcharge_amount=0)
                ),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(
                count=models.Sum(
                    functions.Cast(
                        "selected_rate__meta__surcharge_amount",
                        models.FloatField(),
                    ),
                )
            )
            .order_by("-date")
        )

        members = org.users.count()
        total_errors = sum(
            [item["count"] for item in api_errors if item["count"] is not None], 0
        )
        total_requests = sum(
            [item["count"] for item in api_requests if item["count"] is not None], 0
        )
        total_trackers = sum(
            [item["count"] for item in tracker_count if item["count"] is not None], 0
        )
        total_shipments = sum(
            [item["count"] for item in shipment_count if item["count"] is not None], 0
        )
        order_volume = lib.to_money(
            sum(
                [item["count"] for item in order_volumes if item["count"] is not None],
                0.0,
            )
        )
        unfulfilled_orders = org.orders.filter(
            status__in=["unfulfilled", "partial"], **_test_filter
        ).count()
        total_shipping_spend = lib.to_money(
            sum(
                [item["count"] for item in shipping_spend if item["count"] is not None],
                0.0,
            )
        )
        total_addons_charges = lib.to_money(
            sum(
                [item["count"] for item in addons_charges if item["count"] is not None],
                0.0,
            )
        )

        return dict(
            members=members,
            total_errors=total_errors,
            order_volume=order_volume,
            total_requests=total_requests,
            total_trackers=total_trackers,
            total_shipments=total_shipments,
            unfulfilled_orders=unfulfilled_orders,
            total_shipping_spend=total_shipping_spend,
            total_addons_charges=total_addons_charges,
            api_errors=[utils.UsageStatType.parse(item) for item in api_errors],
            api_requests=[utils.UsageStatType.parse(item) for item in api_requests],
            order_volumes=[utils.UsageStatType.parse(item) for item in order_volumes],
            shipment_count=[utils.UsageStatType.parse(item) for item in shipment_count],
            shipping_spend=[utils.UsageStatType.parse(item) for item in shipping_spend],
            tracker_count=[utils.UsageStatType.parse(item) for item in tracker_count],
        )

    @staticmethod
    @utils.authentication_required
    def resolve(
        info,
        filter: inputs.OrgUsageFilter = strawberry.UNSET,
    ) -> "OrgUsageType":
        _filter = filter.to_dict() if not utils.is_unset(filter) else {}

        org = models.Organization.objects.get(
            is_active=True,
            id=_filter.pop("id"),
            users__id=info.context.request.user.id,
        )
        usage = OrgUsageType.resolve_usage(
            info, org, filter=utils.UsageFilter(**_filter)
        )

        return OrgUsageType(**usage)
