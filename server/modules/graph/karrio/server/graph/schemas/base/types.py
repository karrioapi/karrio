import pydoc
import typing
import datetime
import strawberry
from strawberry.types import Info
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from karrio.server.core import gateway
import karrio.lib as lib
import karrio.server.core.filters as filters
import karrio.server.serializers as serializers
import karrio.server.user.serializers as user_serializers
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.tracing.models as tracing
import karrio.server.graph.models as graph
import karrio.server.core.models as core
import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base.inputs as inputs

User = get_user_model()


@strawberry.type
class UserType:
    email: str
    full_name: str
    is_staff: bool
    date_joined: datetime.datetime
    last_login: typing.Optional[datetime.datetime] = strawberry.UNSET

    @staticmethod
    @utils.authentication_required
    def resolve(info) -> typing.Optional["UserType"]:
        return User.objects.get(id=info.context.request.user.id)


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
        queryset = tracing.TracingRecord.objects.filter(
            meta__request_log_id__icontains=self.id
        )

        if User.objects.filter(
            id=info.context.request.user.id, is_staff=False
        ).exists():
            # exclude system carriers records if user is not staff
            system_carriers = [
                item["id"]
                for item in providers.Carrier.objects.filter(
                    created_by__isnull=True
                ).values("id")
            ]
            queryset = queryset.exclude(meta__carrier_account_id__in=system_carriers)

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
    created: datetime.datetime

    @staticmethod
    @utils.authentication_required
    def resolve(info, org_id: typing.Optional[str] = strawberry.UNSET) -> "TokenType":
        return user_serializers.TokenSerializer.retrieve_token(
            info.context.request,
            **({"org_id": org_id} if org_id is not strawberry.UNSET else {}),
        )


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
    id: str
    object_type: str
    weight: float
    quantity: int
    metadata: utils.JSON
    sku: typing.Optional[str]
    hs_code: typing.Optional[str]
    description: typing.Optional[str]
    value_amount: typing.Optional[float]
    weight_unit: typing.Optional[utils.WeightUnitEnum]
    origin_country: typing.Optional[utils.CountryCodeEnum]
    value_currency: typing.Optional[utils.CurrencyCodeEnum]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]
    parent_id: typing.Optional[str] = None
    parent: typing.Optional["CommodityType"] = None


@strawberry.type
class AddressType:
    id: str
    object_type: str
    postal_code: typing.Optional[str]
    city: typing.Optional[str]
    federal_tax_id: typing.Optional[str]
    state_tax_id: typing.Optional[str]
    person_name: typing.Optional[str]
    company_name: typing.Optional[str]
    country_code: utils.CountryCodeEnum
    email: typing.Optional[str]
    phone_number: typing.Optional[str]
    state_code: typing.Optional[str]
    suburb: typing.Optional[str]
    residential: typing.Optional[bool]
    address_line1: typing.Optional[str]
    address_line2: typing.Optional[str]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]
    validate_location: typing.Optional[bool]
    validation: typing.Optional[utils.JSON] = None


@strawberry.type
class ParcelType:
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
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: UserType

    @strawberry.field
    def items(self: manager.Parcel) -> typing.List[CommodityType]:
        return self.items.all()


@strawberry.type
class DutyType:
    paid_by: typing.Optional[utils.PaidByEnum] = None
    currency: typing.Optional[utils.CurrencyCodeEnum] = None
    account_number: typing.Optional[str] = None
    declared_value: typing.Optional[float] = None
    bill_to: typing.Optional[AddressType] = None


@strawberry.type
class CustomsType:
    id: str
    object_type: str
    certify: typing.Optional[bool] = strawberry.UNSET
    commercial_invoice: typing.Optional[bool] = strawberry.UNSET
    content_type: typing.Optional[utils.CustomsContentTypeEnum] = strawberry.UNSET
    content_description: typing.Optional[str] = strawberry.UNSET
    incoterm: typing.Optional[utils.IncotermCodeEnum] = strawberry.UNSET
    invoice: typing.Optional[str] = strawberry.UNSET
    invoice_date: typing.Optional[datetime.date] = strawberry.UNSET
    signer: typing.Optional[str] = strawberry.UNSET
    created_at: typing.Optional[datetime.datetime] = strawberry.UNSET
    updated_at: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_by: typing.Optional[UserType] = strawberry.UNSET
    options: typing.Optional[utils.JSON] = strawberry.UNSET
    duty_billing_address: typing.Optional[AddressType]

    @strawberry.field
    def duty(self: manager) -> typing.Optional[DutyType]:
        if self.duty is None:
            return None

        return DutyType(**self.duty)

    @strawberry.field
    def commodities(self: manager.Customs) -> typing.List[CommodityType]:
        return self.commodities.all()


@strawberry.type
class AddressTemplateType:
    id: str
    object_type: str
    label: str
    address: AddressType
    is_default: typing.Optional[bool] = None

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AddressFilter] = strawberry.UNSET,
    ) -> utils.Connection["AddressTemplateType"]:
        _filter = inputs.AddressFilter() if utils.is_unset(filter) else filter
        _query = {
            **(  # type: ignore
                {"label__icontain": _filter.label}
                if _filter.label != strawberry.UNSET
                else {}
            ),
            **(
                {"address__icontain": _filter.address}
                if _filter.address != strawberry.UNSET
                else {}
            ),
        }
        queryset = graph.Template.access_by(info.context.request).filter(
            address__isnull=False, **_query
        )

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class ParcelTemplateType:
    id: str
    object_type: str
    label: str
    parcel: ParcelType
    is_default: typing.Optional[bool]

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.TemplateFilter] = strawberry.UNSET,
    ) -> utils.Connection["ParcelTemplateType"]:
        _filter = inputs.TemplateFilter() if filter == strawberry.UNSET else filter

        queryset = graph.Template.access_by(info.context.request).filter(
            parcel__isnull=False,
            **(
                {"label__icontain": _filter.label}
                if _filter.label != strawberry.UNSET
                else {}
            ),
        )
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class CustomsTemplateType:
    id: str
    object_type: str
    label: str
    customs: CustomsType
    is_default: typing.Optional[bool]

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.TemplateFilter] = strawberry.UNSET,
    ) -> utils.Connection["CustomsTemplateType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.TemplateFilter()

        queryset = graph.Template.access_by(info.context.request).filter(
            customs__isnull=False,
            **(
                {"label__icontain": _filter.label}
                if _filter.label is not strawberry.UNSET
                else {}
            ),
        )
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class DefaultTemplatesType:
    default_address: typing.Optional[AddressTemplateType] = None
    default_customs: typing.Optional[CustomsTemplateType] = None
    default_parcel: typing.Optional[ParcelTemplateType] = None

    @staticmethod
    @utils.authentication_required
    def resolve(info) -> "DefaultTemplatesType":
        templates = graph.Template.access_by(info.context.request).filter(
            is_default=True
        )

        return DefaultTemplatesType(  # type: ignore
            default_address=templates.filter(address__isnull=False).first(),
            default_customs=templates.filter(customs__isnull=False).first(),
            default_parcel=templates.filter(parcel__isnull=False).first(),
        )


@strawberry.type
class TrackingEventType:
    description: typing.Optional[str] = None
    location: typing.Optional[str] = None
    code: typing.Optional[str] = None
    date: typing.Optional[str] = None
    time: typing.Optional[str] = None

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
class TrackerType:
    id: str
    object_type: str
    tracking_number: str
    test_mode: bool
    metadata: utils.JSON
    status: utils.TrackerStatusEnum
    delivered: typing.Optional[bool]
    estimated_delivery: typing.Optional[datetime.date]
    options: typing.Optional[utils.JSON]
    meta: typing.Optional[utils.JSON]
    shipment: typing.Optional["ShipmentType"]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: UserType

    @strawberry.field
    def carrier_id(self: manager.Tracking) -> str:
        return getattr(self.tracking_carrier, "carrier_id", None)

    @strawberry.field
    def carrier_name(self: manager.Tracking) -> str:
        return getattr(self.tracking_carrier, "carrier_name", None)

    @strawberry.field
    def events(self: manager.Tracking) -> typing.List[TrackingEventType]:
        return [TrackingEventType.parse(msg) for msg in self.events or []]

    @strawberry.field
    def messages(self: manager.Tracking) -> typing.List[MessageType]:
        return [MessageType.parse(msg) for msg in self.messages or []]

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
class PaymentType:
    account_number: typing.Optional[str] = None
    paid_by: typing.Optional[utils.PaidByEnum] = None
    currency: typing.Optional[utils.CurrencyCodeEnum] = None


@strawberry.type
class ShipmentType:
    id: str
    object_type: str
    test_mode: bool
    shipper: AddressType
    recipient: AddressType
    options: utils.JSON
    metadata: utils.JSON
    status: utils.ShipmentStatusEnum
    meta: typing.Optional[utils.JSON]
    label_type: typing.Optional[utils.LabelTypeEnum]
    tracking_number: typing.Optional[str]
    shipment_identifier: typing.Optional[str]
    tracking_url: typing.Optional[str]
    reference: typing.Optional[str]
    billing_address: typing.Optional[AddressType]
    customs: typing.Optional[CustomsType]
    services: typing.Optional[typing.List[str]]
    service: typing.Optional[str]
    carrier_ids: typing.List[str]
    selected_rate_id: typing.Optional[str]
    tracker_id: typing.Optional[str]
    label_url: typing.Optional[str]
    invoice_url: typing.Optional[str]
    tracker: typing.Optional[TrackerType]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: UserType

    @strawberry.field
    def carrier_id(self: manager.Shipment) -> typing.Optional[str]:
        return getattr(self.selected_rate_carrier, "carrier_id", None)

    @strawberry.field
    def carrier_name(self: manager.Shipment) -> typing.Optional[str]:
        return getattr(self.selected_rate_carrier, "carrier_name", None)

    @strawberry.field
    def parcels(self: manager.Shipment) -> typing.List[ParcelType]:
        return self.parcels.all()

    @strawberry.field
    def rates(self: manager.Shipment) -> typing.List[RateType]:
        return [RateType.parse(rate) for rate in self.rates or []]

    @strawberry.field
    def selected_rate(self: manager.Shipment) -> typing.Optional[RateType]:
        return RateType.parse(self.selected_rate) if self.selected_rate else None

    @strawberry.field
    def payment(self: manager.Shipment) -> typing.Optional[PaymentType]:
        return PaymentType(**self.payment) if self.payment else None

    @strawberry.field
    def messages(self: manager.Tracking) -> typing.List[MessageType]:
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


@strawberry.type
class ServiceLevelType:
    id: str
    object_type: str
    service_name: typing.Optional[str]
    service_code: typing.Optional[str]
    description: typing.Optional[str]
    active: typing.Optional[bool]

    cost: typing.Optional[float]
    currency: typing.Optional[utils.CurrencyCodeEnum]

    estimated_transit_days: typing.Optional[int]

    max_weight: typing.Optional[float]
    max_width: typing.Optional[float]
    max_height: typing.Optional[float]
    max_length: typing.Optional[float]
    weight_unit: typing.Optional[utils.WeightUnitEnum]
    dimension_unit: typing.Optional[utils.DimensionUnitEnum]

    domicile: typing.Optional[bool]
    international: typing.Optional[bool]


@strawberry.type
class LabelTemplateType:
    id: str
    object_type: str
    slug: typing.Optional[str]
    template: typing.Optional[str]
    template_type: typing.Optional[utils.LabelTemplateTypeEnum]
    width: typing.Optional[int]
    height: typing.Optional[int]
    shipment_sample: typing.Optional[utils.JSON]


@strawberry.type
class SystemConnectionType:
    id: str
    active: bool
    carrier_id: str
    test_mode: bool
    capabilities: typing.List[str]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]

    @strawberry.field
    def carrier_name(self: providers.Carrier) -> str:
        return getattr(self, "settings", self).carrier_name

    @strawberry.field
    def display_name(self: providers.Carrier) -> str:
        return getattr(self, "carrier_display_name", "")

    @strawberry.field
    def enabled(self: providers.Carrier, info: Info) -> bool:
        if hasattr(self, "active_orgs"):
            return self.active_orgs.filter(id=info.context.request.org.id).exists()

        return self.active_users.filter(id=info.context.request.user.id).exists()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        test_mode: typing.Optional[bool] = strawberry.UNSET,
    ) -> typing.List["SystemConnectionType"]:
        return gateway.Carriers.list(
            info.context.request,
            system_only=True,
            **(dict(test_mode=test_mode) if test_mode != strawberry.UNSET else {}),
        )


@strawberry.interface
class ConnectionType:
    id: str
    active: bool
    carrier_id: str
    carrier_name: str
    display_name: str
    capabilities: typing.List[str]
    test_mode: bool

    @staticmethod
    @utils.authentication_required
    def resolve_list(info) -> typing.List["CarrierConnectionType"]:
        connections = providers.Carrier.access_by(info.context.request).filter(
            created_by__isnull=False,
            test_mode=getattr(info.context.request, "test_mode", False),
        )

        return list(map(ConnectionType.parse, connections))

    @staticmethod
    def parse(carrier: providers.Carrier) -> "CarrierConnectionType":
        carrier_name = (
            carrier.carrier_name
            if carrier.carrier_name in providers.MODELS
            else "generic"
        )
        _RawSettings = pydoc.locate(f"karrio.mappers.{carrier_name}.Settings")
        settings = {
            key: getattr(carrier.settings, key)
            for key in model_to_dict(carrier.settings).keys()
            if key in _RawSettings.__annotations__
        }
        services = (
            dict(services=carrier.settings.services.all())
            if "services" in settings
            else {}
        )
        display_name = dict(display_name=carrier.carrier_display_name)

        return CarrierSettings[carrier_name](
            id=carrier.id,
            active=carrier.active,
            carrier_name=carrier_name,
            capabilities=carrier.capabilities,
            **{**settings, **services, **display_name},
        )


def create_carrier_settings_type(name: str, model):
    _RawSettings = pydoc.locate(f"karrio.mappers.{name}.Settings")

    @strawberry.type
    class _Settings(ConnectionType):
        metadata: utils.JSON = strawberry.UNSET

        if hasattr(model, "account_number"):
            account_number: typing.Optional[str] = strawberry.UNSET

        if hasattr(model, "account_country_code"):
            account_country_code: typing.Optional[str] = strawberry.UNSET

        if hasattr(model, "label_template"):
            label_template: typing.Optional[LabelTemplateType] = strawberry.UNSET

        if hasattr(model, "services"):

            @strawberry.field
            def services(
                self: providers.Carrier,
            ) -> typing.Optional[typing.List[ServiceLevelType]]:
                return self.services.all()

    annotations = {
        **getattr(_RawSettings, "__annotations__", {}),
        **getattr(_Settings, "__annotations__", {}),
        **(
            dict(services=typing.Optional[typing.List[ServiceLevelType]])
            if hasattr(model, "services")
            else {}
        ),
    }

    return strawberry.type(
        type(
            f"{model.__name__}Type",
            (_Settings,),
            {
                **{
                    k: strawberry.UNSET
                    for k, _ in getattr(_RawSettings, "__annotations__", {}).items()
                    if hasattr(model, k)
                },
                "__annotations__": {
                    k: (
                        typing.Optional[v]
                        if serializers.is_field_optional(model, k)
                        else v
                    )
                    for k, v in annotations.items()
                    if hasattr(model, k)
                },
            },
        )
    )


CarrierSettings = {
    name: create_carrier_settings_type(name, model)
    for name, model in providers.MODELS.items()
}
CarrierConnectionType: typing.Any = strawberry.union(
    "CarrierConnectionType", types=(*(T for T in CarrierSettings.values()),)
)
