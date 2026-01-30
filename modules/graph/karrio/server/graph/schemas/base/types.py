import typing
import datetime
import strawberry
from itertools import groupby
from operator import itemgetter
import django.db.models as models
import django.db.models.functions as functions
from django.conf import settings
from strawberry.types import Info
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.user.models as auth
import karrio.server.core.models as core
import karrio.server.graph.utils as utils
import karrio.server.graph.models as graph
import karrio.server.core.filters as filters
import karrio.server.orders.models as orders
import karrio.server.manager.models as manager
import karrio.server.tracing.models as tracing
import karrio.server.providers.models as providers
import karrio.server.orders.filters as order_filters
import karrio.server.user.serializers as user_serializers
import karrio.server.graph.schemas.base.inputs as inputs
from karrio.server.core.logging import logger

User = get_user_model()


@strawberry.type
class UserType:
    email: str
    full_name: str
    is_staff: bool
    is_active: bool
    date_joined: datetime.datetime
    is_superuser: typing.Optional[bool] = strawberry.UNSET
    last_login: typing.Optional[datetime.datetime] = strawberry.UNSET

    @strawberry.field
    def permissions(self: User, info) -> typing.Optional[typing.List[str]]:
        # Return permissions from token if exists
        if hasattr(getattr(info.context.request, "token", None), "permissions"):
            return info.context.request.token.permissions

        # Return permissions from user
        return info.context.request.user.permissions

    @staticmethod
    @utils.authentication_required
    def resolve(info) -> typing.Optional["UserType"]:
        return User.objects.get(id=info.context.request.user.id)


@strawberry.type
class WorkspaceConfigType:
    object_type: str

    @property
    def config(self: auth.WorkspaceConfig) -> dict:
        try:
            return lib.to_dict(self.config)
        except:
            return self.config

    # general preferences
    # region

    @strawberry.field
    def default_currency(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.CurrencyCodeEnum]:
        return self.config.get("default_currency")

    @strawberry.field
    def default_country_code(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.CountryCodeEnum]:
        return self.config.get("default_country_code")

    @strawberry.field
    def default_weight_unit(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.WeightUnitEnum]:
        return self.config.get("default_weight_unit")

    @strawberry.field
    def default_dimension_unit(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.DimensionUnitEnum]:
        return self.config.get("default_dimension_unit")

    @strawberry.field
    def state_tax_id(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("state_tax_id")

    @strawberry.field
    def federal_tax_id(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("federal_tax_id")

    @strawberry.field
    def default_label_type(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.LabelTypeEnum]:
        return self.config.get("default_label_type")

    # endregion

    # default options preferences
    # region

    @strawberry.field
    def insured_by_default(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("insured_by_default")

    # endregion

    # customs identifiers
    # region

    @strawberry.field
    def customs_aes(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("customs_aes")

    @strawberry.field
    def customs_eel_pfc(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("customs_eel_pfc")

    @strawberry.field
    def customs_license_number(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("customs_license_number")

    @strawberry.field
    def customs_certificate_number(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("customs_certificate_number")

    @strawberry.field
    def customs_nip_number(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("customs_nip_number")

    @strawberry.field
    def customs_eori_number(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("customs_eori_number")

    @strawberry.field
    def customs_vat_registration_number(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[str]:
        return self.config.get("customs_vat_registration_number")

    # endregion

    # label printing
    # region

    @strawberry.field
    def label_message_1(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("label_message_1")

    @strawberry.field
    def label_message_2(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("label_message_2")

    @strawberry.field
    def label_message_3(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("label_message_3")

    @strawberry.field
    def label_logo(self: auth.WorkspaceConfig) -> typing.Optional[str]:
        return self.config.get("label_logo")

    # endregion

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Labels (format uses default_label_type above)
    # ─────────────────────────────────────────────────────────────────
    # region

    @strawberry.field
    def print_label_size(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.LabelSizeEnum]:
        return self.config.get("print_label_size")

    @strawberry.field
    def print_label_show_options(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("print_label_show_options")

    # endregion

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Return Labels
    # ─────────────────────────────────────────────────────────────────
    # region

    @strawberry.field
    def print_return_label_size(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.LabelSizeEnum]:
        return self.config.get("print_return_label_size")

    @strawberry.field
    def print_return_label_show_options(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("print_return_label_show_options")

    # endregion

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Customs Documents
    # ─────────────────────────────────────────────────────────────────
    # region

    @strawberry.field
    def print_customs_size(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.LabelSizeEnum]:
        return self.config.get("print_customs_size")

    @strawberry.field
    def print_customs_show_options(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("print_customs_show_options")

    @strawberry.field
    def print_customs_with_label(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("print_customs_with_label")

    @strawberry.field
    def print_customs_copies(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[int]:
        return self.config.get("print_customs_copies")

    # endregion

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Settings
    # ─────────────────────────────────────────────────────────────────
    # region

    @strawberry.field
    def default_parcel_weight(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[float]:
        return self.config.get("default_parcel_weight")

    @strawberry.field
    def default_shipping_service(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[str]:
        return self.config.get("default_shipping_service")

    @strawberry.field
    def default_shipping_carrier(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[str]:
        return self.config.get("default_shipping_carrier")

    @strawberry.field
    def default_export_reason(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.ExportReasonEnum]:
        return self.config.get("default_export_reason")

    @strawberry.field
    def default_delivery_instructions(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[str]:
        return self.config.get("default_delivery_instructions")

    # endregion

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Label Options
    # ─────────────────────────────────────────────────────────────────
    # region

    @strawberry.field
    def label_show_postage_paid_logo(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("label_show_postage_paid_logo")

    @strawberry.field
    def label_show_qr_code(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("label_show_qr_code")

    @strawberry.field
    def customs_use_order_as_invoice(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("customs_use_order_as_invoice")

    # endregion

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Recommendations Preferences
    # ─────────────────────────────────────────────────────────────────
    # region

    @strawberry.field
    def pref_first_mile(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[typing.List[utils.FirstMileEnum]]:
        return self.config.get("pref_first_mile")

    @strawberry.field
    def pref_last_mile(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[typing.List[utils.LastMileEnum]]:
        return self.config.get("pref_last_mile")

    @strawberry.field
    def pref_form_factor(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[typing.List[utils.FormFactorEnum]]:
        return self.config.get("pref_form_factor")

    @strawberry.field
    def pref_age_check(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[utils.AgeCheckEnum]:
        return self.config.get("pref_age_check")

    @strawberry.field
    def pref_signature_required(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[bool]:
        return self.config.get("pref_signature_required")

    @strawberry.field
    def pref_max_lead_time_days(
        self: auth.WorkspaceConfig,
    ) -> typing.Optional[int]:
        return self.config.get("pref_max_lead_time_days")

    # endregion

    @staticmethod
    @utils.authentication_required
    def resolve(info) -> typing.Optional["WorkspaceConfigType"]:
        workspace_config = auth.WorkspaceConfig.access_by(info.context.request).first()

        # Create a default workspace config if none exists
        if workspace_config is None:
            workspace_config = auth.WorkspaceConfig.objects.create(
                created_by=info.context.request.user, config={}
            )

        return workspace_config


@strawberry.type
class SystemUsageType:
    total_errors: typing.Optional[int] = None
    order_volume: typing.Optional[float] = None
    total_requests: typing.Optional[int] = None
    total_trackers: typing.Optional[int] = None
    total_shipments: typing.Optional[int] = None
    organization_count: typing.Optional[int] = None
    user_count: typing.Optional[int] = None
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
        # Calculate order volumes from JSONField (line_items is embedded JSON)
        _compute_total = lambda items: sum(
            float(i.get("value_amount") or 0) * float(i.get("quantity") or 1)
            for i in (items or [])
        )
        orders_with_totals = [
            (o["date"], _compute_total(o.get("line_items")))
            for o in order_filters.OrderFilters(
                dict(
                    created_before=_filter["date_before"],
                    created_after=_filter["date_after"],
                ),
                orders.Order.objects.filter(**_test_filter).exclude(
                    status__in=["cancelled", "unfulfilled"]
                ),
            )
            .qs.annotate(date=functions.TruncDay("created_at"))
            .values("date", "line_items")
            .order_by("-date")
        ]
        order_volumes = [
            {"date": date, "count": sum(t for _, t in items)}
            for date, items in groupby(orders_with_totals, key=itemgetter(0))
        ]
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
                count=models.Count("id"),
                amount=models.Sum(
                    functions.Cast("selected_rate__total_charge", models.FloatField())
                ),
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
        order_volume = lib.to_decimal(
            sum(
                [item["count"] for item in order_volumes if item["count"] is not None],
                0.0,
            )
        )
        total_shipping_spend = lib.to_decimal(
            sum(
                [
                    item["amount"]
                    for item in shipping_spend
                    if item["amount"] is not None
                ],
                0.0,
            )
        )
        user_count = User.objects.count()
        organization_count = 1

        if conf.settings.MULTI_ORGANIZATIONS:
            import karrio.server.orgs.models as orgs

            organization_count = orgs.Organization.objects.count()

        return SystemUsageType(
            user_count=user_count,
            order_volume=order_volume,
            total_errors=total_errors,
            total_requests=total_requests,
            total_trackers=total_trackers,
            total_shipments=total_shipments,
            organization_count=organization_count,
            total_shipping_spend=total_shipping_spend,
            api_errors=[
                utils.UsageStatType.parse(item, label="api_errors")
                for item in api_errors
            ],
            api_requests=[
                utils.UsageStatType.parse(item, label="api_requests")
                for item in api_requests
            ],
            order_volumes=[
                utils.UsageStatType.parse(item, label="order_volumes")
                for item in order_volumes
            ],
            shipment_count=[
                utils.UsageStatType.parse(item, label="shipment_count")
                for item in shipment_count
            ],
            shipping_spend=[
                utils.UsageStatType.parse(item, label="shipping_spend")
                for item in shipping_spend
            ],
            tracker_count=[
                utils.UsageStatType.parse(item, label="tracker_count")
                for item in tracker_count
            ],
        )


@strawberry.type
class MetafieldType:
    id: str
    key: str
    is_required: bool
    type: utils.MetafieldTypeEnum
    value: typing.Optional[utils.JSON] = None
    object_id: typing.Optional[str] = None

    @strawberry.field
    def object_type(self: core.Metafield) -> str:
        """Return the model name of the attached object, or 'metafield' if not attached."""
        if self.content_type:
            return self.content_type.model
        return "metafield"

    @strawberry.field
    def parsed_value(self: core.Metafield) -> typing.Optional[utils.JSON]:
        """Return the value parsed according to its type."""
        return self.get_parsed_value()

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["MetafieldType"]:
        return core.Metafield.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.MetafieldFilter] = strawberry.UNSET,
    ) -> utils.Connection["MetafieldType"]:
        from django.contrib.contenttypes.models import ContentType

        _filter = filter if not utils.is_unset(filter) else inputs.MetafieldFilter()
        queryset = core.Metafield.access_by(info.context.request)

        # Apply filters
        if not utils.is_unset(_filter.key):
            queryset = queryset.filter(key__icontains=_filter.key)
        if not utils.is_unset(_filter.type):
            queryset = queryset.filter(type=_filter.type)
        if not utils.is_unset(_filter.is_required):
            queryset = queryset.filter(is_required=_filter.is_required)
        if not utils.is_unset(_filter.object_type):
            ct = ContentType.objects.filter(model=_filter.object_type).first()
            if ct:
                queryset = queryset.filter(content_type=ct)
            else:
                queryset = queryset.none()
        if not utils.is_unset(_filter.object_id):
            queryset = queryset.filter(object_id=_filter.object_id)

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class LogType:
    object_type: str
    id: int
    user: typing.Optional[UserType]
    requested_at: typing.Optional[datetime.datetime]
    response_ms: typing.Optional[int]
    path: typing.Optional[str]
    remote_addr: typing.Optional[str]
    host: typing.Optional[str]
    method: typing.Optional[str]
    status_code: typing.Optional[int]
    test_mode: typing.Optional[bool]

    @strawberry.field
    def data(self: core.APILog) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.data)
        except:
            return self.data

    @strawberry.field
    def response(self: core.APILog) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.response)
        except:
            return self.response

    @strawberry.field
    def query_params(self: core.APILog) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.query_params)
        except:
            return self.query_params

    @strawberry.field
    def records(
        self: tracing.TracingRecord, info: Info
    ) -> typing.List["TracingRecordType"]:
        queryset = tracing.TracingRecord.objects.filter(meta__request_log_id=self.id)

        if User.objects.filter(
            id=info.context.request.user.id, is_staff=False
        ).exists():
            # exclude system connection records if user is not staff
            system_connection_ids = list(
                providers.SystemConnection.objects.values_list("id", flat=True)
            )
            queryset = queryset.exclude(meta__carrier_account_id__in=system_connection_ids)

        return queryset

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: int) -> typing.Optional["LogType"]:
        return core.APILogIndex.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.LogFilter] = strawberry.UNSET,
    ) -> utils.Connection["LogType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.LogFilter()
        queryset = filters.LogFilter(
            _filter.to_dict(), core.APILogIndex.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class TracingRecordType:
    object_type: str
    id: typing.Optional[str]
    key: typing.Optional[str]
    timestamp: typing.Optional[float]
    test_mode: typing.Optional[bool]
    created_by: typing.Optional[UserType]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]

    @strawberry.field
    def record(self: tracing.TracingRecord) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.record)
        except:
            return self.record

    @strawberry.field
    def meta(self: tracing.TracingRecord) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.meta)
        except:
            return self.meta

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["TracingRecordType"]:
        return (
            tracing.TracingRecord.access_by(info.context.request).filter(id=id).first()
        )

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.TracingRecordFilter] = strawberry.UNSET,
    ) -> utils.Connection["TracingRecordType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.TracingRecordFilter()
        queryset = filters.TracingRecordFilter(
            _filter.to_dict(), tracing.TracingRecord.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class TokenType:
    object_type: str
    key: str
    label: str
    test_mode: bool
    created: datetime.datetime

    @strawberry.field
    def permissions(self: auth.Token, info) -> typing.Optional[typing.List[str]]:
        # self is a Token model instance, permissions is a @property on the model
        return self.permissions

    @staticmethod
    @utils.authentication_required
    def resolve(info, org_id: typing.Optional[str] = strawberry.UNSET) -> "TokenType":
        return user_serializers.TokenSerializer.retrieve_token(
            info.context.request,
            **({"org_id": org_id} if org_id is not strawberry.UNSET else {}),
        )


@strawberry.type
class APIKeyType:
    object_type: str
    key: str
    label: str
    test_mode: bool
    created: datetime.datetime

    @strawberry.field
    def permissions(self: auth.Token, info) -> typing.Optional[typing.List[str]]:
        # self is a Token model instance, permissions is a @property on the model
        return self.permissions

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
    ) -> typing.List["APIKeyType"]:
        _filters = {
            "user__id": info.context.request.user.id,
            "test_mode": info.context.request.test_mode,
            **(
                {"org__id": info.context.request.org.id}
                if getattr(info.context.request, "org", None) is not None
                and settings.MULTI_ORGANIZATIONS
                else {}
            ),
        }
        keys = auth.Token.objects.filter(**_filters)

        if keys.exists():
            return keys

        user_serializers.TokenSerializer.map(
            data={}, context=info.context.request
        ).save()

        return auth.Token.objects.filter(**_filters)


@strawberry.type
class MessageType:
    carrier_name: typing.Optional[str]
    carrier_id: typing.Optional[str]
    message: typing.Optional[str]
    code: typing.Optional[str]
    details: typing.Optional[utils.JSON] = None

    @staticmethod
    def parse(charge: dict):
        return MessageType(
            **{k: v for k, v in charge.items() if k in MessageType.__annotations__}
        )


@strawberry.type
class ChargeType:
    name: typing.Optional[str] = None
    amount: typing.Optional[float] = None
    currency: utils.CurrencyCodeEnum = None
    id: typing.Optional[str] = None

    @staticmethod
    def parse(charge: dict):
        return ChargeType(
            **{k: v for k, v in charge.items() if k in ChargeType.__annotations__}
        )


@strawberry.type
class RateType:
    id: str
    object_type: str
    carrier_name: str
    carrier_id: str
    service: str
    test_mode: bool
    total_charge: float
    currency: utils.CurrencyCodeEnum
    extra_charges: typing.List[ChargeType]
    meta: typing.Optional[utils.JSON] = None
    transit_days: typing.Optional[int] = None

    @staticmethod
    def parse(rate: dict):
        return RateType(
            **{
                "object_type": "rate",
                **{k: v for k, v in rate.items() if k in RateType.__annotations__},
                "extra_charges": [
                    ChargeType.parse(charge)
                    for charge in (rate.get("extra_charges") or [])
                ],
            }
        )


@strawberry.type
class CommodityType:
    id: typing.Optional[str] = None
    object_type: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    quantity: typing.Optional[int] = None
    metadata: typing.Optional[utils.JSON] = None
    sku: typing.Optional[str] = None
    title: typing.Optional[str] = None
    hs_code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    value_amount: typing.Optional[float] = None
    weight_unit: typing.Optional[utils.WeightUnitEnum] = None
    origin_country: typing.Optional[utils.CountryCodeEnum] = None
    value_currency: typing.Optional[utils.CurrencyCodeEnum] = None
    created_at: typing.Optional[datetime.datetime] = None
    updated_at: typing.Optional[datetime.datetime] = None
    created_by: typing.Optional[UserType] = None
    parent_id: typing.Optional[str] = None
    parent: typing.Optional["CommodityType"] = None
    unfulfilled_quantity: typing.Optional[int] = None

    @staticmethod
    def parse(item: dict) -> typing.Optional["CommodityType"]:
        if not item:
            return None
        return CommodityType(
            **{
                "object_type": item.get("object_type", "commodity"),
                "weight": item.get("weight") or 0,
                "quantity": item.get("quantity") or 1,
                "metadata": item.get("metadata") or {},
                **{k: v for k, v in item.items() if k in CommodityType.__annotations__},
            }
        )


@strawberry.type
class AddressType:
    id: typing.Optional[str] = None
    object_type: typing.Optional[str] = None
    postal_code: typing.Optional[str] = None
    city: typing.Optional[str] = None
    federal_tax_id: typing.Optional[str] = None
    state_tax_id: typing.Optional[str] = None
    person_name: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    country_code: typing.Optional[utils.CountryCodeEnum] = None
    email: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    state_code: typing.Optional[str] = None
    residential: typing.Optional[bool] = None
    street_number: typing.Optional[str] = None
    address_line1: typing.Optional[str] = None
    address_line2: typing.Optional[str] = None
    created_at: typing.Optional[datetime.datetime] = None
    updated_at: typing.Optional[datetime.datetime] = None
    created_by: typing.Optional[UserType] = None
    validate_location: typing.Optional[bool] = None
    validation: typing.Optional[utils.JSON] = None

    @staticmethod
    def parse(address: dict) -> typing.Optional["AddressType"]:
        if not address:
            return None
        return AddressType(
            **{
                "object_type": address.get("object_type", "address"),
                **{k: v for k, v in address.items() if k in AddressType.__annotations__},
            }
        )


@strawberry.type
class ParcelType:
    id: typing.Optional[str] = None
    object_type: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    length: typing.Optional[float] = None
    packaging_type: typing.Optional[str] = None
    package_preset: typing.Optional[str] = None
    description: typing.Optional[str] = None
    content: typing.Optional[str] = None
    is_document: typing.Optional[bool] = None
    weight_unit: typing.Optional[utils.WeightUnitEnum] = None
    dimension_unit: typing.Optional[utils.DimensionUnitEnum] = None
    freight_class: typing.Optional[str] = None
    reference_number: typing.Optional[str] = None
    created_at: typing.Optional[datetime.datetime] = None
    updated_at: typing.Optional[datetime.datetime] = None
    created_by: typing.Optional[UserType] = None
    items: typing.Optional[typing.List[CommodityType]] = None

    @staticmethod
    def parse(parcel: dict) -> typing.Optional["ParcelType"]:
        if not parcel:
            return None
        return ParcelType(
            **{
                "object_type": parcel.get("object_type", "parcel"),
                **{k: v for k, v in parcel.items() if k in ParcelType.__annotations__ and k != "items"},
                "items": [CommodityType.parse(i) for i in (parcel.get("items") or [])],
            }
        )


@strawberry.type
class DutyType:
    paid_by: typing.Optional[utils.PaidByEnum] = None
    currency: typing.Optional[utils.CurrencyCodeEnum] = None
    account_number: typing.Optional[str] = None
    declared_value: typing.Optional[float] = None
    bill_to: typing.Optional[AddressType] = None

    @staticmethod
    def parse(duty: dict) -> typing.Optional["DutyType"]:
        if not duty:
            return None
        return DutyType(
            paid_by=duty.get("paid_by"),
            currency=duty.get("currency"),
            account_number=duty.get("account_number"),
            declared_value=duty.get("declared_value"),
            bill_to=AddressType.parse(duty.get("bill_to")),
        )


@strawberry.type
class CustomsType:
    """Customs type for embedded JSON customs data on shipments.

    This is a pure data type that parses customs JSON data, not tied to a database model.
    """
    certify: typing.Optional[bool] = None
    commercial_invoice: typing.Optional[bool] = None
    content_type: typing.Optional[utils.CustomsContentTypeEnum] = None
    content_description: typing.Optional[str] = None
    incoterm: typing.Optional[utils.IncotermCodeEnum] = None
    invoice: typing.Optional[str] = None
    invoice_date: typing.Optional[str] = None
    signer: typing.Optional[str] = None
    options: typing.Optional[utils.JSON] = None
    # Private fields for parsed nested objects
    _duty: strawberry.Private[typing.Optional[DutyType]] = None
    _duty_billing_address: strawberry.Private[typing.Optional[AddressType]] = None
    _commodities: strawberry.Private[typing.Optional[typing.List[CommodityType]]] = None

    @strawberry.field
    def duty(self) -> typing.Optional[DutyType]:
        return self._duty

    @strawberry.field
    def duty_billing_address(self) -> typing.Optional[AddressType]:
        return self._duty_billing_address

    @strawberry.field
    def commodities(self) -> typing.Optional[typing.List[CommodityType]]:
        return self._commodities

    @staticmethod
    def parse(customs: dict) -> typing.Optional["CustomsType"]:
        if not customs:
            return None
        return CustomsType(
            certify=customs.get("certify"),
            commercial_invoice=customs.get("commercial_invoice"),
            content_type=customs.get("content_type"),
            content_description=customs.get("content_description"),
            incoterm=customs.get("incoterm"),
            invoice=customs.get("invoice"),
            invoice_date=customs.get("invoice_date"),
            signer=customs.get("signer"),
            options=customs.get("options"),
            _duty=DutyType.parse(customs.get("duty")),
            _duty_billing_address=AddressType.parse(customs.get("duty_billing_address")),
            _commodities=[CommodityType.parse(c) for c in (customs.get("commodities") or [])],
        )


@strawberry.type
class AddressTemplateType:
    """Address template type for reusable address templates.

    Uses the Address model directly with meta.label for template metadata,
    following the PRD pattern for direct model templates.
    All fields are resolved from the Django model's properties.
    """

    id: str
    object_type: str
    postal_code: typing.Optional[str]
    city: typing.Optional[str]
    federal_tax_id: typing.Optional[str]
    state_tax_id: typing.Optional[str]
    person_name: typing.Optional[str]
    company_name: typing.Optional[str]
    country_code: typing.Optional[utils.CountryCodeEnum]
    email: typing.Optional[str]
    phone_number: typing.Optional[str]
    state_code: typing.Optional[str]
    residential: typing.Optional[bool]
    street_number: typing.Optional[str]
    address_line1: typing.Optional[str]
    address_line2: typing.Optional[str]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]
    validate_location: typing.Optional[bool]
    validation: typing.Optional[utils.JSON]
    meta: typing.Optional[utils.JSON] = None


# Standalone resolver functions for saved addresses (AddressTemplateType)
@utils.authentication_required
def resolve_addresses(
    info,
    filter: typing.Optional[inputs.AddressFilter] = strawberry.UNSET,
) -> utils.Connection[AddressTemplateType]:
    """Resolver for listing saved addresses."""
    _filter = inputs.AddressFilter() if utils.is_unset(filter) else filter
    _search = _filter.to_dict()
    _query = models.Q(meta__label__isnull=False) & ~models.Q(meta__label="")

    if any(_search.get("label") or ""):
        _value = _search.get("label")
        _query = _query & models.Q(meta__label__icontains=_value)

    if any(_search.get("address") or ""):
        _value = _search.get("address")
        _query = _query & (
            models.Q(address_line1__icontains=_value)
            | models.Q(address_line2__icontains=_value)
            | models.Q(postal_code__icontains=_value)
            | models.Q(person_name__icontains=_value)
            | models.Q(company_name__icontains=_value)
            | models.Q(country_code__icontains=_value)
            | models.Q(city__icontains=_value)
            | models.Q(email__icontains=_value)
            | models.Q(phone_number__icontains=_value)
        )

    if any(_search.get("keyword") or ""):
        _value = _search.get("keyword")
        _query = _query & (
            models.Q(meta__label__icontains=_value)
            | models.Q(address_line1__icontains=_value)
            | models.Q(address_line2__icontains=_value)
            | models.Q(postal_code__icontains=_value)
            | models.Q(person_name__icontains=_value)
            | models.Q(company_name__icontains=_value)
            | models.Q(country_code__icontains=_value)
            | models.Q(city__icontains=_value)
            | models.Q(email__icontains=_value)
            | models.Q(phone_number__icontains=_value)
        )

    if any(_search.get("usage") or ""):
        _value = _search.get("usage")
        _query = _query & models.Q(meta__usage__contains=_value)

    queryset = manager.Address.access_by(info.context.request).filter(_query)

    return utils.paginated_connection(queryset, **_filter.pagination())


@utils.authentication_required
def resolve_address(info, id: str) -> typing.Optional[AddressTemplateType]:
    """Resolver for getting a single saved address by ID."""
    return manager.Address.access_by(info.context.request).filter(
        id=id,
        meta__label__isnull=False,
    ).first()


@strawberry.type
class ParcelTemplateType:
    """Parcel template type for reusable parcel templates.

    Uses the Parcel model directly with meta.label for template metadata,
    following the PRD pattern for direct model templates.
    All fields are resolved from the Django model's properties.
    """

    id: str
    object_type: str
    weight: typing.Optional[float]
    width: typing.Optional[float]
    height: typing.Optional[float]
    length: typing.Optional[float]
    packaging_type: typing.Optional[str]
    package_preset: typing.Optional[str]
    description: typing.Optional[str]
    content: typing.Optional[str]
    is_document: typing.Optional[bool]
    weight_unit: typing.Optional[utils.WeightUnitEnum]
    dimension_unit: typing.Optional[utils.DimensionUnitEnum]
    freight_class: typing.Optional[str]
    reference_number: typing.Optional[str]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]
    meta: typing.Optional[utils.JSON] = None

    @strawberry.field
    def items(self: manager.Parcel) -> typing.Optional[typing.List[CommodityType]]:
        """Items in the parcel."""
        items_rel = getattr(self, "items", None)
        if items_rel is None:
            return None
        if hasattr(items_rel, "all"):
            return list(items_rel.all())
        return items_rel


# Standalone resolver functions for saved parcels (ParcelTemplateType)
@utils.authentication_required
def resolve_parcels(
    info,
    filter: typing.Optional[inputs.TemplateFilter] = strawberry.UNSET,
) -> utils.Connection[ParcelTemplateType]:
    """Resolver for listing saved parcels."""
    _filter = inputs.TemplateFilter() if filter == strawberry.UNSET else filter
    _search = _filter.to_dict()
    _query = models.Q(meta__label__isnull=False) & ~models.Q(meta__label="")

    if any(_search.get("label") or ""):
        _value = _search.get("label")
        _query = _query & models.Q(meta__label__icontains=_value)

    if any(_search.get("keyword") or ""):
        _value = _search.get("keyword")
        _query = _query & models.Q(meta__label__icontains=_value)

    if any(_search.get("usage") or ""):
        _value = _search.get("usage")
        _query = _query & models.Q(meta__usage__contains=_value)

    queryset = manager.Parcel.access_by(info.context.request).filter(_query)

    return utils.paginated_connection(queryset, **_filter.pagination())


@utils.authentication_required
def resolve_parcel(info, id: str) -> typing.Optional[ParcelTemplateType]:
    """Resolver for getting a single saved parcel by ID."""
    return manager.Parcel.access_by(info.context.request).filter(
        id=id,
        meta__label__isnull=False,
    ).first()


@strawberry.type
class ProductTemplateType:
    """Product template type for reusable product/commodity templates.

    Uses the Commodity model directly with meta.label for template metadata,
    following the PRD pattern for direct model templates.
    All fields are resolved from the Django model's properties.
    """

    id: str
    object_type: str
    weight: float
    quantity: int
    sku: typing.Optional[str]
    title: typing.Optional[str]
    hs_code: typing.Optional[str]
    description: typing.Optional[str]
    value_amount: typing.Optional[float]
    weight_unit: typing.Optional[utils.WeightUnitEnum]
    origin_country: typing.Optional[utils.CountryCodeEnum]
    value_currency: typing.Optional[utils.CurrencyCodeEnum]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]
    metadata: typing.Optional[utils.JSON] = None
    meta: typing.Optional[utils.JSON] = None


# Standalone resolver functions for saved products (ProductTemplateType)
@utils.authentication_required
def resolve_products(
    info,
    filter: typing.Optional[inputs.ProductFilter] = strawberry.UNSET,
) -> utils.Connection[ProductTemplateType]:
    """Resolver for listing saved products."""
    _filter = filter if not utils.is_unset(filter) else inputs.ProductFilter()
    _search = _filter.to_dict()
    _query = models.Q(meta__label__isnull=False) & ~models.Q(meta__label="")

    if any(_search.get("label") or ""):
        _value = _search.get("label")
        _query = _query & models.Q(meta__label__icontains=_value)

    if any(_search.get("keyword") or ""):
        _value = _search.get("keyword")
        _query = _query & (
            models.Q(meta__label__icontains=_value)
            | models.Q(title__icontains=_value)
            | models.Q(sku__icontains=_value)
            | models.Q(description__icontains=_value)
            | models.Q(hs_code__icontains=_value)
        )

    if any(_search.get("sku") or ""):
        _value = _search.get("sku")
        _query = _query & models.Q(sku__icontains=_value)

    if _search.get("origin_country"):
        _query = _query & models.Q(origin_country=_search.get("origin_country"))

    if any(_search.get("usage") or ""):
        _value = _search.get("usage")
        _query = _query & models.Q(meta__usage__contains=_value)

    queryset = manager.Commodity.access_by(info.context.request).filter(_query)

    return utils.paginated_connection(queryset, **_filter.pagination())


@utils.authentication_required
def resolve_product(info, id: str) -> typing.Optional[ProductTemplateType]:
    """Resolver for getting a single saved product by ID."""
    return manager.Commodity.access_by(info.context.request).filter(
        id=id,
        meta__label__isnull=False,
    ).first()


@strawberry.type
class DefaultTemplatesType:
    """Default templates type for user's default address, parcel, and product templates.

    Uses strawberry.Private to store the actual model instances and @strawberry.field
    methods to return them as the correct strawberry types, ensuring proper field resolution.
    """

    _default_address: strawberry.Private[typing.Optional[manager.Address]] = None
    _default_parcel: strawberry.Private[typing.Optional[manager.Parcel]] = None
    _default_product: strawberry.Private[typing.Optional[manager.Commodity]] = None

    @strawberry.field
    def default_address(self) -> typing.Optional[AddressTemplateType]:
        """Returns the default address template."""
        return self._default_address  # type: ignore

    @strawberry.field
    def default_parcel(self) -> typing.Optional[ParcelTemplateType]:
        """Returns the default parcel template."""
        return self._default_parcel  # type: ignore

    @strawberry.field
    def default_product(self) -> typing.Optional[ProductTemplateType]:
        """Returns the default product template."""
        return self._default_product  # type: ignore


# Standalone resolver function for DefaultTemplatesType
@utils.authentication_required
def resolve_default_templates(info) -> DefaultTemplatesType:
    """Resolver for getting default templates."""
    default_address = manager.Address.access_by(info.context.request).filter(
        meta__is_default=True,
        meta__label__isnull=False,
    ).first()
    default_parcel = manager.Parcel.access_by(info.context.request).filter(
        meta__is_default=True,
        meta__label__isnull=False,
    ).first()
    default_product = manager.Commodity.access_by(info.context.request).filter(
        meta__is_default=True,
        meta__label__isnull=False,
    ).first()

    return DefaultTemplatesType(
        _default_address=default_address,
        _default_parcel=default_parcel,
        _default_product=default_product,
    )


@strawberry.type
class TrackingEventType:
    description: typing.Optional[str] = None
    location: typing.Optional[str] = None
    code: typing.Optional[str] = None
    date: typing.Optional[str] = None
    time: typing.Optional[str] = None
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None

    @staticmethod
    def parse(charge: dict):
        return TrackingEventType(
            **{
                k: v
                for k, v in charge.items()
                if k in TrackingEventType.__annotations__
            }
        )


@strawberry.type
class TrackingInfoType:
    carrier_tracking_link: typing.Optional[str] = None
    customer_name: typing.Optional[str] = None
    expected_delivery: typing.Optional[str] = None
    note: typing.Optional[str] = None
    order_date: typing.Optional[str] = None
    order_id: typing.Optional[str] = None
    package_weight: typing.Optional[str] = None
    package_weight_unit: typing.Optional[str] = None
    shipment_package_count: typing.Optional[str] = None
    shipment_pickup_date: typing.Optional[str] = None
    shipment_delivery_date: typing.Optional[str] = None
    shipment_service: typing.Optional[str] = None
    shipment_origin_country: typing.Optional[str] = None
    shipment_origin_postal_code: typing.Optional[str] = None
    shipment_destination_country: typing.Optional[str] = None
    shipment_destination_postal_code: typing.Optional[str] = None
    shipping_date: typing.Optional[str] = None
    signed_by: typing.Optional[str] = None
    source: typing.Optional[str] = None

    @staticmethod
    def parse(charge: dict):
        return TrackingInfoType(
            **{k: v for k, v in charge.items() if k in TrackingInfoType.__annotations__}
        )


@strawberry.type
class CarrierSnapshotType:
    """Represents a carrier snapshot stored at the time of operation."""

    connection_id: typing.Optional[str] = None
    connection_type: typing.Optional[str] = None
    carrier_code: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    carrier_name: typing.Optional[str] = None
    test_mode: typing.Optional[bool] = None

    @staticmethod
    def parse(
        snapshot: typing.Optional[dict],
    ) -> typing.Optional["CarrierSnapshotType"]:
        if not snapshot:
            return None
        return CarrierSnapshotType(
            connection_id=snapshot.get("connection_id"),
            connection_type=snapshot.get("connection_type"),
            carrier_code=snapshot.get("carrier_code"),
            carrier_id=snapshot.get("carrier_id"),
            carrier_name=snapshot.get("carrier_name"),
            test_mode=snapshot.get("test_mode"),
        )


@strawberry.type
class TrackerType:
    id: str
    object_type: str
    tracking_number: str
    test_mode: bool
    metadata: utils.JSON
    status: utils.TrackerStatusEnum
    delivered: typing.Optional[bool]
    estimated_delivery: typing.Optional[datetime.date]
    document_image_url: typing.Optional[str]
    signature_image_url: typing.Optional[str]
    options: typing.Optional[utils.JSON]
    meta: typing.Optional[utils.JSON]
    shipment: typing.Optional["ShipmentType"]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: UserType

    @strawberry.field
    def carrier_id(self: manager.Tracking) -> typing.Optional[str]:
        return (self.carrier or {}).get("carrier_id")

    @strawberry.field
    def carrier_name(self: manager.Tracking) -> typing.Optional[str]:
        return (self.carrier or {}).get("carrier_name")

    @strawberry.field
    def info(self: manager.Tracking) -> typing.Optional[TrackingInfoType]:
        return TrackingInfoType.parse(self.info) if self.info else None

    @strawberry.field
    def events(self: manager.Tracking) -> typing.List[TrackingEventType]:
        return [TrackingEventType.parse(msg) for msg in self.events or []]

    @strawberry.field
    def messages(self: manager.Tracking) -> typing.List[MessageType]:
        return [MessageType.parse(msg) for msg in self.messages or []]

    @strawberry.field
    def tracking_carrier(
        self: manager.Tracking,
    ) -> typing.Optional[CarrierSnapshotType]:
        return CarrierSnapshotType.parse(self.carrier)

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["TrackerType"]:
        return manager.Tracking.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.TrackerFilter] = strawberry.UNSET,
    ) -> utils.Connection["TrackerType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.TrackerFilter()
        queryset = filters.TrackerFilters(
            _filter.to_dict(), manager.Tracking.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class ManifestType:
    id: str
    object_type: str
    test_mode: bool
    metadata: utils.JSON
    meta: utils.JSON
    options: utils.JSON
    address: AddressType
    shipment_identifiers: typing.List[str]
    manifest_url: typing.Optional[str]
    reference: typing.Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @strawberry.field
    def carrier_id(self: manager.Manifest) -> typing.Optional[str]:
        return (self.carrier or {}).get("carrier_id")

    @strawberry.field
    def carrier_name(self: manager.Manifest) -> typing.Optional[str]:
        return (self.carrier or {}).get("carrier_name")

    @strawberry.field
    def messages(self: manager.Manifest) -> typing.List[MessageType]:
        return [MessageType.parse(msg) for msg in self.messages or []]

    @strawberry.field
    def manifest_carrier(
        self: manager.Manifest,
    ) -> typing.Optional[CarrierSnapshotType]:
        return CarrierSnapshotType.parse(self.carrier)

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["ManifestType"]:
        return manager.Manifest.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.ManifestFilter] = strawberry.UNSET,
    ) -> utils.Connection["ManifestType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.ManifestFilter()
        queryset = filters.ManifestFilters(
            _filter.to_dict(), manager.Manifest.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class PickupType:
    """GraphQL type for Pickup model."""

    id: str
    object_type: str
    confirmation_number: typing.Optional[str]
    pickup_date: typing.Optional[str]
    ready_time: typing.Optional[str]
    closing_time: typing.Optional[str]
    instruction: typing.Optional[str]
    package_location: typing.Optional[str]
    test_mode: bool
    options: utils.JSON
    metadata: utils.JSON
    meta: typing.Optional[utils.JSON]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: UserType

    @strawberry.field
    def pickup_type(self: manager.Pickup) -> str:
        """Pickup scheduling type: one_time, daily, or recurring."""
        return self.pickup_type or "one_time"

    @strawberry.field
    def recurrence(self: manager.Pickup) -> typing.Optional[utils.JSON]:
        """Recurrence config for recurring pickups."""
        return self.recurrence

    @strawberry.field
    def carrier_id(self: manager.Pickup) -> typing.Optional[str]:
        return (self.carrier or {}).get("carrier_id")

    @strawberry.field
    def carrier_name(self: manager.Pickup) -> typing.Optional[str]:
        return (self.carrier or {}).get("carrier_name")

    @strawberry.field
    def address(self: manager.Pickup) -> typing.Optional[AddressType]:
        return AddressType.parse(self.address) if self.address else None

    @strawberry.field
    def pickup_charge(self: manager.Pickup) -> typing.Optional[ChargeType]:
        return ChargeType.parse(self.pickup_charge) if self.pickup_charge else None

    @strawberry.field
    def parcels(self: manager.Pickup) -> typing.List[ParcelType]:
        """Parcels from related shipments."""
        return [
            ParcelType.parse(p)
            for shipment in self.shipments.all()
            for p in (shipment.parcels or [])
        ]

    @strawberry.field
    def tracking_numbers(self: manager.Pickup) -> typing.List[str]:
        """Tracking numbers from related shipments."""
        return [
            s.tracking_number
            for s in self.shipments.all()
            if s.tracking_number
        ]

    @strawberry.field
    def shipments(self: manager.Pickup) -> typing.List["ShipmentType"]:
        """Related shipments for this pickup."""
        return list(self.shipments.all())

    @strawberry.field
    def pickup_carrier(
        self: manager.Pickup,
    ) -> typing.Optional[CarrierSnapshotType]:
        """Carrier snapshot with credentials protected."""
        return CarrierSnapshotType.parse(self.carrier)

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["PickupType"]:
        return manager.Pickup.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.PickupFilter] = strawberry.UNSET,
    ) -> utils.Connection["PickupType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.PickupFilter()
        queryset = filters.PickupFilters(
            _filter.to_dict(), manager.Pickup.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class PaymentType:
    account_number: typing.Optional[str] = None
    paid_by: typing.Optional[utils.PaidByEnum] = None
    currency: typing.Optional[utils.CurrencyCodeEnum] = None

@strawberry.type
class ShipmentType:
    id: str
    object_type: str
    test_mode: bool
    options: utils.JSON
    metadata: utils.JSON
    status: utils.ShipmentStatusEnum
    meta: typing.Optional[utils.JSON]
    label_type: typing.Optional[utils.LabelTypeEnum]
    tracking_number: typing.Optional[str]
    shipment_identifier: typing.Optional[str]
    tracking_url: typing.Optional[str]
    reference: typing.Optional[str]
    services: typing.Optional[typing.List[str]]
    service: typing.Optional[str]
    selected_rate_id: typing.Optional[str]
    tracker_id: typing.Optional[str]
    label_url: typing.Optional[str]
    invoice_url: typing.Optional[str]
    tracker: typing.Optional[TrackerType]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: UserType

    @strawberry.field
    def shipper(self: manager.Shipment) -> AddressType:
        return AddressType.parse(self.shipper)

    @strawberry.field
    def recipient(self: manager.Shipment) -> AddressType:
        return AddressType.parse(self.recipient)

    @strawberry.field
    def return_address(self: manager.Shipment) -> typing.Optional[AddressType]:
        return AddressType.parse(self.return_address)

    @strawberry.field
    def billing_address(self: manager.Shipment) -> typing.Optional[AddressType]:
        return AddressType.parse(self.billing_address)

    @strawberry.field
    def customs(self: manager.Shipment) -> typing.Optional[CustomsType]:
        return CustomsType.parse(self.customs)

    @strawberry.field
    def carrier_id(self: manager.Shipment) -> typing.Optional[str]:
        if self.selected_rate is None:
            return None
        return self.selected_rate.get("carrier_id")

    @strawberry.field
    def carrier_name(self: manager.Shipment) -> typing.Optional[str]:
        if self.selected_rate is None:
            return None
        return self.selected_rate.get("carrier_name")

    @strawberry.field
    def carrier_ids(self: manager.Shipment) -> typing.List[str]:
        return self.carrier_ids or []

    @strawberry.field
    def parcels(self: manager.Shipment) -> typing.List[ParcelType]:
        # parcels is now a JSON field, return parsed ParcelType objects
        return [ParcelType.parse(p) for p in (self.parcels or [])]

    @strawberry.field
    def rates(self: manager.Shipment) -> typing.List[RateType]:
        return [RateType.parse(rate) for rate in self.rates or []]

    @strawberry.field
    def selected_rate(self: manager.Shipment) -> typing.Optional[RateType]:
        return RateType.parse(self.selected_rate) if self.selected_rate else None

    @strawberry.field
    def selected_rate_carrier(
        self: manager.Shipment,
    ) -> typing.Optional[CarrierSnapshotType]:
        if self.carrier is None:
            return None
        return CarrierSnapshotType.parse(self.carrier)

    @strawberry.field
    def payment(self: manager.Shipment) -> typing.Optional[PaymentType]:
        return PaymentType(**self.payment) if self.payment else None

    @strawberry.field
    def messages(self: manager.Shipment) -> typing.List[MessageType]:
        return [MessageType.parse(msg) for msg in self.messages or []]

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["ShipmentType"]:
        return manager.Shipment.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.ShipmentFilter] = strawberry.UNSET,
    ) -> utils.Connection["ShipmentType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.ShipmentFilter()
        queryset = filters.ShipmentFilters(
            _filter.to_dict(), manager.Shipment.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


# ─────────────────────────────────────────────────────────────────────────────
# SHARED ZONE TYPE (Rate Sheet Level)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class SharedZoneType:
    """Shared zone definition at the RateSheet level."""

    object_type: str
    id: str
    label: typing.Optional[str] = None

    transit_days: typing.Optional[int] = None
    transit_time: typing.Optional[float] = None

    radius: typing.Optional[float] = None
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None

    cities: typing.Optional[typing.List[str]] = None
    postal_codes: typing.Optional[typing.List[str]] = None
    country_codes: typing.Optional[typing.List[str]] = None

    # Weight constraints for this zone
    min_weight: typing.Optional[float] = None
    max_weight: typing.Optional[float] = None
    weight_unit: typing.Optional[utils.WeightUnitEnum] = None

    @staticmethod
    def parse(zone: dict):
        return SharedZoneType(
            object_type="shared_zone",
            id=zone.get("id", ""),
            label=zone.get("label"),
            transit_days=zone.get("transit_days"),
            transit_time=zone.get("transit_time"),
            radius=zone.get("radius"),
            latitude=zone.get("latitude"),
            longitude=zone.get("longitude"),
            cities=zone.get("cities"),
            postal_codes=zone.get("postal_codes"),
            country_codes=zone.get("country_codes"),
            min_weight=zone.get("min_weight"),
            max_weight=zone.get("max_weight"),
            weight_unit=zone.get("weight_unit"),
        )


# ─────────────────────────────────────────────────────────────────────────────
# SHARED SURCHARGE TYPE (Rate Sheet Level)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class SharedSurchargeType:
    """Shared surcharge definition at the RateSheet level."""

    object_type: str
    id: str
    name: str
    amount: float
    surcharge_type: str
    cost: typing.Optional[float] = None
    active: bool = True

    @staticmethod
    def parse(surcharge: dict):
        return SharedSurchargeType(
            object_type="shared_surcharge",
            id=surcharge.get("id", ""),
            name=surcharge.get("name", ""),
            amount=float(surcharge.get("amount", 0)),
            surcharge_type=surcharge.get("surcharge_type", "fixed"),
            cost=surcharge.get("cost"),
            active=surcharge.get("active", True),
        )


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE RATE TYPE (Service-Zone Rate Mapping)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.type
class ServiceRateType:
    """Service-zone rate mapping."""

    object_type: str
    service_id: str
    zone_id: str
    rate: float
    cost: typing.Optional[float] = None
    min_weight: typing.Optional[float] = None
    max_weight: typing.Optional[float] = None
    transit_days: typing.Optional[int] = None
    transit_time: typing.Optional[float] = None

    @staticmethod
    def parse(rate: dict):
        return ServiceRateType(
            object_type="service_rate",
            service_id=rate.get("service_id", ""),
            zone_id=rate.get("zone_id", ""),
            rate=float(rate.get("rate", 0)),
            cost=rate.get("cost"),
            min_weight=rate.get("min_weight"),
            max_weight=rate.get("max_weight"),
            transit_days=rate.get("transit_days"),
            transit_time=rate.get("transit_time"),
        )


@strawberry.type
class ServiceLevelFeaturesType:
    """Structured service level features.

    Defines the capabilities and characteristics of a shipping service.
    Used for filtering, display, and setting default options.
    """

    # First Mile: How parcels get to the carrier
    # "pick_up" | "drop_off" | "pick_up_and_drop_off"
    first_mile: typing.Optional[str] = None

    # Last Mile: How parcels are delivered to recipient
    # "home_delivery" | "service_point" | "mailbox"
    last_mile: typing.Optional[str] = None

    # Form Factor: Type of package the service supports
    # "letter" | "parcel" | "mailbox" | "pallet"
    form_factor: typing.Optional[str] = None

    # Type of Shipments: Business model support
    b2c: typing.Optional[bool] = None  # Business to Consumer
    b2b: typing.Optional[bool] = None  # Business to Business

    # Shipment Direction: "outbound" | "returns" | "both"
    shipment_type: typing.Optional[str] = None

    # Age Verification: null | "16" | "18"
    age_check: typing.Optional[str] = None

    # Default signature requirement
    signature: typing.Optional[bool] = None

    # Tracking availability
    tracked: typing.Optional[bool] = None

    # Insurance availability
    insurance: typing.Optional[bool] = None

    # Express/Priority service
    express: typing.Optional[bool] = None

    # Dangerous goods support
    dangerous_goods: typing.Optional[bool] = None

    # Weekend delivery options
    saturday_delivery: typing.Optional[bool] = None
    sunday_delivery: typing.Optional[bool] = None

    # Multi-package shipment support
    multicollo: typing.Optional[bool] = None

    # Neighbor delivery allowed
    neighbor_delivery: typing.Optional[bool] = None

    @staticmethod
    def parse(features: typing.Optional[dict]) -> "ServiceLevelFeaturesType":
        """Parse a features dict into ServiceLevelFeaturesType."""
        if not features or not isinstance(features, dict):
            return ServiceLevelFeaturesType()

        import dataclasses
        field_names = {f.name for f in dataclasses.fields(ServiceLevelFeaturesType)}
        return ServiceLevelFeaturesType(**{
            k: v for k, v in features.items() if k in field_names
        })


@strawberry.type
class ServiceLevelType:
    """
    Service level definition for rate sheet-based shipping.

    Services reference shared zones and surcharges defined at the RateSheet level
    via zone_ids and surcharge_ids. Rate values are stored in RateSheet.service_rates.
    """

    id: str
    object_type: str
    service_name: typing.Optional[str]
    service_code: typing.Optional[str]
    carrier_service_code: typing.Optional[str]
    description: typing.Optional[str]
    active: typing.Optional[bool]

    currency: typing.Optional[utils.CurrencyCodeEnum]
    transit_days: typing.Optional[int]
    transit_time: typing.Optional[float]

    max_width: typing.Optional[float]
    max_height: typing.Optional[float]
    max_length: typing.Optional[float]
    dimension_unit: typing.Optional[utils.DimensionUnitEnum]

    min_weight: typing.Optional[float]
    max_weight: typing.Optional[float]
    weight_unit: typing.Optional[utils.WeightUnitEnum]

    max_volume: typing.Optional[float]
    cost: typing.Optional[float]

    # Volumetric weight fields
    dim_factor: typing.Optional[float]
    use_volumetric: typing.Optional[bool]

    domicile: typing.Optional[bool]
    international: typing.Optional[bool]

    @strawberry.field
    def features(self: providers.ServiceLevel) -> ServiceLevelFeaturesType:
        """Structured service features."""
        return ServiceLevelFeaturesType.parse(self.features)

    @strawberry.field
    def metadata(self: providers.ServiceLevel) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.metadata)
        except:
            return self.metadata

    @strawberry.field
    def zone_ids(self: providers.ServiceLevel) -> typing.List[str]:
        """List of zone IDs this service applies to (references RateSheet.zones)."""
        return self.zone_ids or []

    @strawberry.field
    def surcharge_ids(self: providers.ServiceLevel) -> typing.List[str]:
        """List of surcharge IDs to apply (references RateSheet.surcharges)."""
        return self.surcharge_ids or []


@strawberry.type
class LabelTemplateType:
    id: str
    object_type: str
    slug: typing.Optional[str]
    template: typing.Optional[str]
    width: typing.Optional[int]
    height: typing.Optional[int]
    shipment_sample: typing.Optional[utils.JSON]
    template_type: typing.Optional[utils.LabelTemplateTypeEnum]


@strawberry.type
class RateSheetType:
    object_type: str
    id: str
    name: str
    slug: str
    carrier_name: utils.CarrierNameEnum

    @strawberry.field
    def origin_countries(self: providers.RateSheet) -> typing.Optional[typing.List[str]]:
        return self.origin_countries or []

    @strawberry.field
    def metadata(self: providers.RateSheet) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.metadata)
        except:
            return self.metadata

    @strawberry.field
    def carriers(self: providers.RateSheet) -> typing.List["CarrierConnectionType"]:
        return self.carriers

    @strawberry.field
    def services(self: providers.RateSheet) -> typing.List[ServiceLevelType]:
        return self.services.all()

    # ─────────────────────────────────────────────────────────────────
    # NEW: Shared zones at RateSheet level
    # ─────────────────────────────────────────────────────────────────
    @strawberry.field
    def zones(self: providers.RateSheet) -> typing.Optional[typing.List[SharedZoneType]]:
        """Shared zone definitions for this rate sheet."""
        zones_data = self.zones or []
        return [SharedZoneType.parse(zone) for zone in zones_data]

    # ─────────────────────────────────────────────────────────────────
    # NEW: Shared surcharges at RateSheet level
    # ─────────────────────────────────────────────────────────────────
    @strawberry.field
    def surcharges(
        self: providers.RateSheet,
    ) -> typing.Optional[typing.List[SharedSurchargeType]]:
        """Shared surcharge definitions for this rate sheet."""
        surcharges_data = self.surcharges or []
        return [SharedSurchargeType.parse(surcharge) for surcharge in surcharges_data]

    # ─────────────────────────────────────────────────────────────────
    # NEW: Service-zone rate mappings
    # ─────────────────────────────────────────────────────────────────
    @strawberry.field
    def service_rates(
        self: providers.RateSheet,
    ) -> typing.Optional[typing.List[ServiceRateType]]:
        """Service-zone rate mappings for this rate sheet."""
        rates_data = self.service_rates or []
        return [ServiceRateType.parse(rate) for rate in rates_data]

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["RateSheetType"]:
        return providers.RateSheet.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.RateSheetFilter] = strawberry.UNSET,
    ) -> utils.Connection["RateSheetType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.RateSheetFilter()
        queryset = filters.RateSheetFilter(
            _filter.to_dict(), providers.RateSheet.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class SystemConnectionType:
    """Represents a SystemConnection that can be enabled by users via BrokeredConnection."""

    id: str
    carrier_id: str
    carrier_code: str
    display_name: str
    test_mode: bool
    capabilities: typing.List[str]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]

    active: bool

    @strawberry.field
    def carrier_name(self: providers.SystemConnection) -> str:
        return self.carrier_code

    @strawberry.field
    def enabled(self: providers.SystemConnection, info: Info) -> bool:
        """Check if this SystemConnection is enabled for the current user/org."""
        if settings.MULTI_ORGANIZATIONS:
            org_id = getattr(info.context.request, "org", None)
            org_id = org_id.id if org_id else None
            return providers.BrokeredConnection.objects.filter(
                system_connection=self,
                is_enabled=True,
                link__org__id=org_id,
            ).exists()
        else:
            user_id = getattr(info.context.request, "user", None)
            user_id = user_id.id if user_id else None
            return providers.BrokeredConnection.objects.filter(
                system_connection=self,
                is_enabled=True,
                created_by__id=user_id,
            ).exists()

    @strawberry.field
    def config(self: providers.SystemConnection, info: Info) -> typing.Optional[utils.JSON]:
        """Get the user's config for this SystemConnection from their BrokeredConnection."""
        if settings.MULTI_ORGANIZATIONS:
            org_id = getattr(info.context.request, "org", None)
            org_id = org_id.id if org_id else None
            brokered = providers.BrokeredConnection.objects.filter(
                system_connection=self,
                link__org__id=org_id,
            ).first()
        else:
            user_id = getattr(info.context.request, "user", None)
            user_id = user_id.id if user_id else None
            brokered = providers.BrokeredConnection.objects.filter(
                system_connection=self,
                created_by__id=user_id,
            ).first()
        return brokered.config if brokered else None

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.CarrierFilter] = strawberry.UNSET,
    ) -> utils.Connection["SystemConnectionType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.CarrierFilter()
        queryset = providers.SystemConnection.objects.filter(
            active=True,
            test_mode=getattr(info.context.request, "test_mode", False),
        )
        # Apply carrier filter if specified
        if _filter.carrier_name:
            queryset = queryset.filter(carrier_code=_filter.carrier_name)
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class CarrierConnectionType:
    """GraphQL type for carrier connections."""

    id: str
    carrier_id: str
    carrier_code: str
    carrier_name: str
    display_name: str
    active: bool
    test_mode: bool
    capabilities: typing.List[str]

    @strawberry.field
    def credentials(self: providers.CarrierConnection, info: Info) -> utils.JSON:
        return self.credentials

    @strawberry.field
    def metadata(self: providers.CarrierConnection, info: Info) -> typing.Optional[utils.JSON]:
        return getattr(self, "metadata", None)

    @strawberry.field
    def config(self: providers.CarrierConnection, info: Info) -> typing.Optional[utils.JSON]:
        return getattr(self, "config", None)

    @strawberry.field
    def rate_sheet(
        self: providers.CarrierConnection, info: Info
    ) -> typing.Optional[RateSheetType]:
        # Access rate_sheet FK from the Django model
        return getattr(self, "rate_sheet", None)

    @staticmethod
    @utils.utils.error_wrapper
    @utils.authentication_required
    def resolve_list_legacy(
        info,
        filter: typing.Optional[inputs.CarrierFilter] = strawberry.UNSET,
    ) -> typing.List["CarrierConnectionType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.CarrierFilter()
        # Carrier model now only contains user/org-owned connections (no is_system filter needed)
        connections = filters.CarrierFilters(
            _filter.to_dict(),
            providers.CarrierConnection.access_by(info.context.request),
        ).qs
        return connections

    @staticmethod
    @utils.utils.error_wrapper
    @utils.authentication_required
    def resolve(
        info,
        id: str,
    ) -> typing.Optional["CarrierConnectionType"]:
        connection = (
            providers.CarrierConnection.access_by(info.context.request).filter(id=id).first()
        )
        return connection

    @staticmethod
    @utils.utils.error_wrapper
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.CarrierFilter] = strawberry.UNSET,
    ) -> utils.Connection["CarrierConnectionType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.CarrierFilter()
        # Carrier model now only contains user/org-owned connections (no is_system filter needed)
        queryset = filters.CarrierFilters(
            _filter.to_dict(),
            providers.CarrierConnection.access_by(info.context.request),
        ).qs
        connections = utils.paginated_connection(queryset, **_filter.pagination())

        return utils.Connection(
            page_info=connections.page_info,
            edges=[
                utils.Edge(
                    node=edge.node,
                    cursor=edge.cursor,
                )
                for edge in connections.edges
            ],
        )
