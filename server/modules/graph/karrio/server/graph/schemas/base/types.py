import pydoc
import typing
import datetime
import strawberry
from strawberry.types import Info
from karrio.server.core import gateway

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from karrio.core.utils import DP
import karrio.server.core.filters as filters
import karrio.server.user.serializers as user_serializers
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.graph.models as graph
import karrio.server.core.models as core
import karrio.server.graph.schemas.utils as utils
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
    @utils.login_required
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

    @strawberry.field
    def data(self: core.APILog) -> typing.Optional[inputs.JSON]:
        try:
            return DP.to_dict(self.data)
        except:
            return self.data

    @strawberry.field
    def response(self: core.APILog) -> typing.Optional[inputs.JSON]:
        try:
            return DP.to_dict(self.response)
        except:
            print("touch")
            return self.response

    @strawberry.field
    def query_params(self: core.APILog) -> typing.Optional[inputs.JSON]:
        try:
            return DP.to_dict(self.query_params)
        except:
            return self.query_params

    @staticmethod
    @utils.login_required
    def resolve(info, id: int) -> typing.Optional["LogType"]:
        return core.APILog.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.login_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.LogFilter] = strawberry.UNSET,
    ) -> utils.Connection["LogType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.LogFilter()
        queryset = filters.LogFilter(
            _filter.to_dict(), core.APILog.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class TokenType:
    object_type: str
    key: str
    created: datetime.datetime

    @staticmethod
    @utils.login_required
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
    details: typing.Optional[inputs.JSON] = strawberry.UNSET


@strawberry.type
class ChargeType:
    name: typing.Optional[str]
    amount: typing.Optional[float]
    currency: inputs.CurrencyCodeEnum


@strawberry.type
class RateType:
    id: typing.Optional[str]
    carrier_name: typing.Optional[str]
    carrier_id: typing.Optional[str]
    currency: inputs.CurrencyCodeEnum
    transit_days: typing.Optional[int]
    service: typing.Optional[str]
    total_charge: typing.Optional[float]
    extra_charges: typing.List[ChargeType]
    test_mode: typing.Optional[bool]
    meta: typing.Optional[inputs.JSON] = strawberry.UNSET


@strawberry.type
class CommodityType:
    object_type: str
    id: typing.Optional[str]
    sku: typing.Optional[str]
    quantity: typing.Optional[int]
    weight: typing.Optional[float]
    description: typing.Optional[str]
    value_amount: typing.Optional[float]
    weight_unit: typing.Optional[inputs.WeightUnitEnum]
    origin_country: typing.Optional[inputs.CountryCodeEnum]
    value_currency: typing.Optional[inputs.CurrencyCodeEnum]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]
    metadata: typing.Optional[inputs.JSON] = strawberry.UNSET
    parent_id: typing.Optional[str] = strawberry.UNSET
    parent: typing.Optional["CommodityType"] = strawberry.UNSET


@strawberry.type
class AddressType:
    object_type: str
    id: typing.Optional[str]
    postal_code: typing.Optional[str]
    city: typing.Optional[str]
    federal_tax_id: typing.Optional[str]
    state_tax_id: typing.Optional[str]
    person_name: typing.Optional[str]
    company_name: typing.Optional[str]
    country_code: typing.Optional[inputs.CountryCodeEnum]
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
    validation: typing.Optional[inputs.JSON] = strawberry.UNSET


@strawberry.type
class ParcelType:
    object_type: str
    id: typing.Optional[str]
    weight: typing.Optional[float]
    width: typing.Optional[float]
    height: typing.Optional[float]
    length: typing.Optional[float]
    packaging_type: typing.Optional[str]
    package_preset: typing.Optional[str]
    description: typing.Optional[str]
    content: typing.Optional[str]
    is_document: typing.Optional[bool]
    weight_unit: typing.Optional[inputs.WeightUnitEnum]
    dimension_unit: typing.Optional[inputs.DimensionUnitEnum]
    reference_number: typing.Optional[str]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]
    items: typing.Optional[typing.List[CommodityType]]


@strawberry.type
class DutyType:
    id: typing.Optional[str]
    paid_by: typing.Optional[inputs.PaidByEnum]
    currency: typing.Optional[inputs.CountryCodeEnum]
    account_number: typing.Optional[str]
    declared_value: typing.Optional[float]
    bill_to: typing.Optional[AddressType] = strawberry.UNSET


@strawberry.type
class CustomsType:
    object_type: str
    id: typing.Optional[str]
    certify: typing.Optional[bool]
    commercial_invoice: typing.Optional[bool]
    content_type: typing.Optional[inputs.CustomsContentTypeEnum]
    content_description: typing.Optional[str]
    incoterm: typing.Optional[inputs.IncotermCodeEnum]
    invoice: typing.Optional[str]
    invoice_date: typing.Optional[datetime.date]
    signer: typing.Optional[str]
    duty: typing.Optional[DutyType]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]
    options: typing.Optional[inputs.JSON] = strawberry.UNSET

    @strawberry.field
    def commodities(self: manager.Customs) -> typing.List[CommodityType]:
        return self.commodities.all()


@strawberry.type
class AddressTemplateType:
    object_type: str
    id: str
    label: str
    address: AddressType
    is_default: typing.Optional[bool]

    @staticmethod
    @utils.login_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.AddressFilter] = strawberry.UNSET,
    ) -> utils.Connection["AddressType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.AddressFilter()
        _query = {
            **(  # type: ignore
                {"label__icontain": filter.label}
                if filter.label is not strawberry.UNSET
                else {}
            )
            ** (
                {"address__icontain": filter.address}
                if filter.address is not strawberry.UNSET
                else {}
            )
        }

        queryset = graph.Template.access_by(info.context).filter(
            address__isnull=False, **_query
        )
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class ParcelTemplateType:
    object_type: str
    id: str
    label: str
    parcel: ParcelType
    is_default: typing.Optional[bool]

    @staticmethod
    @utils.login_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.TemplateFilter] = strawberry.UNSET,
    ) -> utils.Connection["ParcelTemplateType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.TemplateFilter()

        queryset = graph.Template.access_by(info.context).filter(
            parcel__isnull=False,
            **(
                {"label__icontain": filter.label}
                if filter.label is not strawberry.UNSET
                else {}
            ),
        )
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class CustomsTemplateType:
    object_type: str
    id: str
    label: str
    customs: CustomsType
    is_default: typing.Optional[bool]

    @staticmethod
    @utils.login_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.TemplateFilter] = strawberry.UNSET,
    ) -> utils.Connection["CustomsTemplateType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.TemplateFilter()

        queryset = graph.Template.access_by(info.context).filter(
            customs__isnull=False,
            **(
                {"label__icontain": filter.label}
                if filter.label is not strawberry.UNSET
                else {}
            ),
        )
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class DefaultTemplatesType:
    default_address: typing.Optional[AddressTemplateType]
    default_customs: typing.Optional[CustomsTemplateType]
    default_parcel: typing.Optional[ParcelTemplateType]

    @staticmethod
    @utils.login_required
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
    description: typing.Optional[str]
    location: typing.Optional[str]
    code: typing.Optional[str]
    date: typing.Optional[str]
    time: typing.Optional[str]


@strawberry.type
class TrackerType:
    object_type: str
    id: typing.Optional[str]
    tracking_number: typing.Optional[str]
    status: typing.Optional[inputs.TrackerStatusEnum]
    events: typing.Optional[typing.List[TrackingEventType]]
    delivered: typing.Optional[bool]
    estimated_delivery: typing.Optional[datetime.date]
    test_mode: typing.Optional[bool]
    options: typing.Optional[inputs.JSON]
    meta: typing.Optional[inputs.JSON]
    metadata: typing.Optional[inputs.JSON]
    shipment: typing.Optional["ShipmentType"]
    messages: typing.Optional[typing.List[MessageType]]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]

    @strawberry.field
    def carrier_id(self: manager.Customs) -> typing.List[str]:
        return getattr(self.tracking_carrier, "carrier_id", None)

    @strawberry.field
    def carrier_name(self: manager.Customs) -> typing.List[str]:
        return getattr(self.tracking_carrier, "carrier_name", None)

    @staticmethod
    @utils.login_required
    def resolve(info, id: str) -> typing.Optional["TrackerType"]:
        return manager.Tracking.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.login_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.TrackerFilter] = strawberry.UNSET,
    ) -> utils.Connection["TrackerType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.TrackerFilter()
        queryset = filters.TrackerFilter(
            _filter.to_dict(), manager.Tracking.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class PaymentType:
    id: typing.Optional[str]
    account_number: typing.Optional[str]
    paid_by: typing.Optional[inputs.PaidByEnum]
    currency: typing.Optional[inputs.CurrencyCodeEnum]


@strawberry.type
class ShipmentType:
    object_type: str
    id: typing.Optional[str]
    status: typing.Optional[inputs.ShipmentStatusEnum]
    recipient: typing.Optional[AddressType]
    shipper: typing.Optional[AddressType]
    label_type: typing.Optional[inputs.LabelTypeEnum]
    tracking_number: typing.Optional[str]
    shipment_identifier: typing.Optional[str]
    tracking_url: typing.Optional[str]
    test_mode: typing.Optional[bool]
    reference: typing.Optional[str]
    customs: typing.Optional[CustomsType]
    selected_rate: typing.Optional[RateType]
    payment: typing.Optional[PaymentType]
    options: typing.Optional[inputs.JSON]
    services: typing.Optional[typing.List[str]]
    messages: typing.Optional[typing.List[MessageType]]
    meta: typing.Optional[inputs.JSON]
    metadata: typing.Optional[inputs.JSON]
    rates: typing.Optional[typing.List[RateType]]
    parcels: typing.Optional[typing.List[ParcelType]]
    service: typing.Optional[str]
    carrier_ids: typing.Optional[typing.List[str]]
    selected_rate_id: typing.Optional[str]
    tracker_id: typing.Optional[str]
    label_url: typing.Optional[str]
    invoice_url: typing.Optional[str]
    tracker: typing.Optional[TrackerType]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[UserType]

    @strawberry.field
    def carrier_id(self: manager.Customs) -> typing.List[str]:
        return getattr(self.tracking_carrier, "carrier_id", None)

    @strawberry.field
    def carrier_name(self: manager.Customs) -> typing.List[str]:
        return getattr(self.tracking_carrier, "carrier_name", None)

    @staticmethod
    @utils.login_required
    def resolve(info, id: str) -> typing.Optional["ShipmentType"]:
        return manager.Shipment.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.login_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.ShipmentFilter] = strawberry.UNSET,
    ) -> utils.Connection["ShipmentType"]:
        _filter = filter if filter is not strawberry.UNSET else inputs.ShipmentFilter()
        queryset = filters.ShipmentFilter(
            _filter.to_dict(), manager.Shipment.access_by(info.context.request)
        ).qs
        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class ServiceLevelType:
    object_type: str
    id: typing.Optional[str]
    service_name: typing.Optional[str]
    service_code: typing.Optional[str]
    description: typing.Optional[str]
    active: typing.Optional[bool]

    cost: typing.Optional[float]
    currency: typing.Optional[inputs.CurrencyCodeEnum]

    estimated_transit_days: typing.Optional[int]

    max_weight: typing.Optional[float]
    max_width: typing.Optional[float]
    max_height: typing.Optional[float]
    max_length: typing.Optional[float]
    weight_unit: typing.Optional[inputs.WeightUnitEnum]
    dimension_unit: typing.Optional[inputs.DimensionUnitEnum]

    domicile: typing.Optional[bool]
    international: typing.Optional[bool]


@strawberry.type
class LabelTemplateType:
    object_type: str
    id: typing.Optional[str]
    slug: typing.Optional[str]
    template: typing.Optional[str]
    template_type: typing.Optional[inputs.LabelTemplateTypeEnum]
    width: typing.Optional[int]
    height: typing.Optional[int]
    shipment_sample: typing.Optional[inputs.JSON]


@strawberry.type
class SystemConnectionType:
    id: typing.Optional[str]
    carrier_id: typing.Optional[str]
    test: typing.Optional[bool]
    active: typing.Optional[bool]
    capabilities: typing.Optional[typing.List[str]]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]

    @strawberry.field
    def carrier_name(self: providers.Carrier) -> typing.Optional[str]:
        return getattr(self, "settings", self).carrier_name

    @strawberry.field
    def enabled(self: providers.Carrier, info: Info) -> typing.Optional[bool]:
        if hasattr(self, "active_orgs"):
            return self.active_orgs.filter(id=info.context.request.org.id).exists()

        return self.active_users.filter(id=info.context.request.user.id).exists()

    @staticmethod
    @utils.login_required
    def resolve_list(
        info,
        test: typing.Optional[bool] = strawberry.UNSET,
    ) -> typing.List["SystemConnectionType"]:
        return gateway.Carriers.list(
            context=info.context.request,
            system_only=True,
            **(dict(test=test) if test != strawberry.UNSET else {}),
        )


@strawberry.interface
class ConnectionType:
    id: typing.Optional[str]

    @strawberry.field
    def carrier_name(self: providers.Carrier) -> typing.Optional[str]:
        return getattr(self, "settings", self).carrier_name

    @staticmethod
    @utils.login_required
    def resolve_list(
        info,
        test: typing.Optional[bool] = strawberry.UNSET,
    ) -> typing.List["ConnectionType"]:
        connections = providers.Carrier.access_by(info.context.request).filter(
            created_by__isnull=False,
            **(dict(test=test) if test != strawberry.UNSET else {}),
        )
        return [connection.settings for connection in connections]


def create_carrier_settings_type(name: str, model):
    _RawSettings = pydoc.locate(f"karrio.mappers.{name}.Settings")

    @strawberry.type
    class _Settings(ConnectionType):
        metadata: typing.Optional[inputs.JSON] = strawberry.UNSET

        if hasattr(model, "account_country_code"):
            account_country_code: str = strawberry.UNSET

        if hasattr(model, "label_template"):
            label_template: typing.Optional[LabelTemplateType] = strawberry.UNSET

        if hasattr(model, "services"):

            @strawberry.field
            def services(self: providers.Carrier) -> typing.List[ServiceLevelType]:
                return self.services.all()

    annotations = {
        **getattr(_RawSettings, "__annotations__", {}),
        **getattr(_Settings, "__annotations__", {}),
    }

    return strawberry.type(
        type(
            f"{model.__name__}Type",
            (_Settings,),
            {
                **{
                    k: strawberry.UNSET
                    for k, _ in getattr(_RawSettings, "__annotations__", {}).items()
                },
                "__annotations__": {
                    k: v for k, v in annotations.items() if k not in ["services"]
                },
            },
        )
    )


CarrierSettings = {
    name: create_carrier_settings_type(name, model)
    for name, model in providers.MODELS.items()
}
