import enum
import pydoc
import typing
import datetime
import strawberry
import dataclasses
from django.conf import settings

from karrio.server.core import serializers
import karrio.server.manager.models as manager
import karrio.server.providers.models as providers

JSON: typing.Any = strawberry.scalar(
    typing.NewType("JSON", object),
    description="The `JSON` scalar type represents JSON values as specified by ECMA-404",
)

CurrencyCodeEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("CurrencyCodeEnum", serializers.CURRENCIES)
)
CountryCodeEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("CountryCodeEnum", serializers.COUNTRIES)
)
DimensionUnitEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("DimensionUnitEnum", serializers.DIMENSION_UNIT)
)
WeightUnitEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("WeightUnitEnum", serializers.WEIGHT_UNIT)
)
CustomsContentTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("CustomsContentTypeEnum", serializers.CUSTOMS_CONTENT_TYPE)
)
IncotermCodeEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("IncotermCodeEnum", serializers.INCOTERMS)
)
PaidByEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("PaidByEnum", serializers.PAYMENT_TYPES)
)
LabelTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("LabelTypeEnum", serializers.LABEL_TYPES)
)
LabelTemplateTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("LabelTemplateTypeEnum", serializers.LABEL_TEMPLATE_TYPES)
)
ShipmentStatusEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("ShipmentStatusEnum", serializers.SHIPMENT_STATUS)
)
TrackerStatusEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("TrackerStatusEnum", serializers.TRACKER_STATUS)
)


def metadata_object_types() -> enum.Enum:
    _types = [
        ("carrier", providers.Carrier),
        ("commodity", manager.Commodity),
        ("shipment", manager.Shipment),
        ("tracker", manager.Tracking),
    ]

    if settings.ORDERS_MANAGEMENT:
        import karrio.server.orders.models as orders

        _types.append(("order", orders.Order))

    if settings.APPS_MANAGEMENT:
        import karrio.server.apps.models as apps

        _types.append(("app", apps.App))

    return enum.Enum("MetadataObjectType", _types)


MetadataObjectTypeEnum: typing.Any = strawberry.enum(metadata_object_types())  # type: ignore


@strawberry.input
class BaseInput:
    def pagination(self) -> typing.Dict[str, typing.Any]:
        return {
            k: v
            for k, v in dataclasses.asdict(self).items()
            if k in ["offset", "before", "after", "first", "last"]
        }

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            k: v
            for k, v in dataclasses.asdict(self).items()
            if v is not strawberry.UNSET
        }


@strawberry.input
class Paginated(BaseInput):
    offset: typing.Optional[int] = strawberry.UNSET
    first: typing.Optional[int] = strawberry.UNSET


@strawberry.input
class LogFilter(Paginated):
    api_endpoint: typing.Optional[str] = strawberry.UNSET
    date_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    date_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    entity_id: typing.Optional[str] = strawberry.UNSET
    method: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[str] = strawberry.UNSET
    status_code: typing.Optional[typing.List[int]] = strawberry.UNSET


@strawberry.input
class TrackerFilter(Paginated):
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[typing.List[str]] = strawberry.UNSET
    test_mode: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class ShipmentFilter(Paginated):
    address: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    reference: typing.Optional[str] = strawberry.UNSET
    service: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[typing.List[str]] = strawberry.UNSET
    option_key: typing.Optional[typing.List[str]] = strawberry.UNSET
    option_value: typing.Optional[str] = strawberry.UNSET
    metadata_key: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata_value: typing.Optional[str] = strawberry.UNSET
    test_mode: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class TemplateFilter(Paginated):
    label: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class AddressFilter(TemplateFilter):
    address: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class UpdateUserInput(BaseInput):
    full_name: typing.Optional[str] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class TokenMutationInput(BaseInput):
    password: typing.Optional[str] = strawberry.UNSET
    refresh: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class EmailChangeMutationInput(BaseInput):
    email: str
    password: str
    redirect_url: str


@strawberry.input
class ConfirmEmailChangeMutationInput(BaseInput):
    token: str


@strawberry.input
class RegisterUserMutationInput(BaseInput):
    email: str
    password1: str
    password2: str
    redirect_url: str
    full_name: typing.Optional[str] = None


@strawberry.input
class ConfirmEmailMutationInput(BaseInput):
    token: str


@strawberry.input
class ChangePasswordMutationInput(BaseInput):
    old_password: str
    new_password1: str
    new_password2: str


@strawberry.input
class ConfirmPasswordResetMutationInput(BaseInput):
    uuid: str
    token: str
    new_password1: str
    new_password2: str


@strawberry.input
class MetadataMutationInput(BaseInput):
    id: str
    object_type: MetadataObjectTypeEnum  # type:ignore
    added_values: "JSON"  # type:ignore
    delete_keys: typing.Optional[typing.List[str]]


@strawberry.input
class CommodityInput:
    sku: typing.Optional[str]
    quantity: typing.Optional[int]
    weight: typing.Optional[float]
    description: typing.Optional[str]
    value_amount: typing.Optional[float]
    weight_unit: typing.Optional[WeightUnitEnum]
    origin_country: typing.Optional[CountryCodeEnum]
    value_currency: typing.Optional[CurrencyCodeEnum]
    metadata: typing.Optional[JSON]
    parent_id: typing.Optional[str]


@strawberry.input
class AddressInput:
    postal_code: typing.Optional[str]
    city: typing.Optional[str]
    federal_tax_id: typing.Optional[str]
    state_tax_id: typing.Optional[str]
    person_name: typing.Optional[str]
    company_name: typing.Optional[str]
    country_code: typing.Optional[CountryCodeEnum]
    email: typing.Optional[str]
    phone_number: typing.Optional[str]
    state_code: typing.Optional[str]
    suburb: typing.Optional[str]
    residential: typing.Optional[bool]
    address_line1: typing.Optional[str]
    address_line2: typing.Optional[str]


@strawberry.input
class ParcelInput:
    weight: typing.Optional[float]
    width: typing.Optional[float]
    height: typing.Optional[float]
    length: typing.Optional[float]
    packaging_type: typing.Optional[str]
    package_preset: typing.Optional[str]
    description: typing.Optional[str]
    content: typing.Optional[str]
    is_document: typing.Optional[bool]
    weight_unit: typing.Optional[WeightUnitEnum]
    dimension_unit: typing.Optional[DimensionUnitEnum]
    reference_number: typing.Optional[str]
    items: typing.Optional[typing.List[CommodityInput]]


@strawberry.input
class DutyInput:
    paid_by: typing.Optional[PaidByEnum]
    currency: typing.Optional[CountryCodeEnum]
    account_number: typing.Optional[str]
    declared_value: typing.Optional[float]
    bill_to: typing.Optional[AddressInput]


@strawberry.input
class CustomsInput:
    certify: typing.Optional[bool]
    commercial_invoice: typing.Optional[bool]
    content_type: typing.Optional[CustomsContentTypeEnum]
    content_description: typing.Optional[str]
    incoterm: typing.Optional[IncotermCodeEnum]
    invoice: typing.Optional[str]
    invoice_date: typing.Optional[datetime.date]
    signer: typing.Optional[str]
    duty: typing.Optional[DutyInput]
    options: typing.Optional[JSON]
    commodities: typing.Optional[typing.List[CommodityInput]]


@strawberry.input
class PaymentInput:
    account_number: typing.Optional[str]
    paid_by: typing.Optional[PaidByEnum]
    currency: typing.Optional[CurrencyCodeEnum]


@strawberry.input
class PartialShipmentMutationInput(BaseInput):
    id: str
    recipient: typing.Optional[AddressInput]
    shipper: typing.Optional[AddressInput]
    customs: typing.Optional[CustomsInput]
    parcels: typing.Optional[typing.List[ParcelInput]]
    payment: typing.Optional[PaymentInput]
    options: typing.Optional[JSON]
    metadata: typing.Optional[JSON]
    reference: typing.Optional[str]


@strawberry.input
class CreateAddressTemplateInput(BaseInput):
    label: str
    address: AddressInput
    is_default: typing.Optional[bool]


@strawberry.input
class UpdateAddressTemplateInput(CreateAddressTemplateInput):
    id: str
    label: typing.Optional[str]
    address: typing.Optional[AddressInput]


@strawberry.input
class CreateCustomsTemplateInput(BaseInput):
    label: str
    customs: CustomsInput
    is_default: typing.Optional[bool]


@strawberry.input
class UpdateCustomsTemplateInput(CreateCustomsTemplateInput):
    id: str
    label: typing.Optional[str]
    customs: typing.Optional[CustomsInput]


@strawberry.input
class CreateParcelTemplateInput(BaseInput):
    label: str
    parcel: ParcelInput
    is_default: typing.Optional[bool]


@strawberry.input
class UpdateParcelTemplateInput(CreateParcelTemplateInput):
    id: str
    label: typing.Optional[str]
    parcel: typing.Optional[ParcelInput]


@strawberry.input
class CreateLabelTemplateInput(BaseInput):
    slug: str
    template: str
    template_type: LabelTemplateTypeEnum
    width: typing.Optional[int]
    height: typing.Optional[int]
    shipment_sample: typing.Optional[JSON]


@strawberry.input
class UpdateLabelTemplateInput(BaseInput):
    id: str
    slug: typing.Optional[str]
    template: typing.Optional[str]
    template_type: typing.Optional[LabelTemplateTypeEnum]


@strawberry.input
class CreateServiceLevelInput(BaseInput):
    service_name: str
    service_code: str
    cost: float
    currency: CurrencyCodeEnum

    description: typing.Optional[str]
    active: typing.Optional[bool]

    estimated_transit_days: typing.Optional[int]

    max_weight: typing.Optional[float]
    max_width: typing.Optional[float]
    max_height: typing.Optional[float]
    max_length: typing.Optional[float]
    weight_unit: typing.Optional[WeightUnitEnum]
    dimension_unit: typing.Optional[DimensionUnitEnum]

    domicile: typing.Optional[bool]
    international: typing.Optional[bool]


@strawberry.input
class UpdateServiceLevelInput(BaseInput):
    id: str
    service_name: typing.Optional[str]
    service_code: typing.Optional[str]
    cost: typing.Optional[float]
    currency: typing.Optional[CurrencyCodeEnum]


def carrier_settings_inputs(is_update: bool = False) -> typing.Dict[str, typing.Type]:
    def carrier_settings_input(name: str, model):
        _name = f"{'Update' if is_update else ''}{model.__name__}Input"
        _RawSettings = pydoc.locate(f"karrio.mappers.{name}.Settings")
        _excluded = ["services", "id"]
        _optionals = ["account_country_code", "label_template"]
        _template_type: typing.Any = (
            "UpdateLabelTemplateInput" if is_update else "CreateLabelTemplateInput"
        )
        _service_type: typing.Any = (
            "UpdateServiceLevelInput" if is_update else "CreateServiceLevelInput"
        )

        @strawberry.input
        class _CarrierInput(BaseInput):
            if is_update:
                id: str = strawberry.UNSET

            if hasattr(model, "account_country_code"):
                account_country_code: typing.Optional[str] = strawberry.UNSET

            if hasattr(model, "label_template"):
                label_template: typing.Optional[_template_type] = strawberry.UNSET

            if hasattr(model, "services"):
                services: typing.Optional[_service_type] = strawberry.UNSET

            metadata: typing.Optional[JSON] = strawberry.UNSET

        annotations = {
            **getattr(_RawSettings, "__annotations__", {}),
            **getattr(_CarrierInput, "__annotations__", {}),
        }

        return strawberry.input(
            type(
                _name,
                (_CarrierInput,),
                {
                    **{
                        k: strawberry.UNSET
                        for k, _ in getattr(_RawSettings, "__annotations__", {}).items()
                    },
                    "__annotations__": {
                        k: typing.Optional[v] if is_update or k in _optionals else v
                        for k, v in annotations.items()
                        if k not in _excluded
                    },
                },
            )
        )

    return {
        name: carrier_settings_input(name, model)
        for name, model in providers.MODELS.items()
    }


CreateCarrierInputs = carrier_settings_inputs()
UpdateCarrierInputs = carrier_settings_inputs(is_update=True)


CreateCarrierConnectionMutationInput = strawberry.input(
    type(
        "CreateCarrierConnectionMutationInput",
        (BaseInput,),
        {
            **{name: strawberry.UNSET for name, type in CreateCarrierInputs.items()},
            "__annotations__": {
                name: typing.Optional[type]
                for name, type in CreateCarrierInputs.items()
            },
        },
    )
)
UpdateCarrierConnectionMutationInput = strawberry.input(
    type(
        "UpdateCarrierConnectionMutationInput",
        (BaseInput,),
        {
            **{name: strawberry.UNSET for name in UpdateCarrierInputs.keys()},
            "__annotations__": {
                name: typing.Optional[type]  # type:ignore
                for name, type in UpdateCarrierInputs.items()
            },
        },
    )
)
