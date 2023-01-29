import pydoc
import typing
import datetime
import strawberry

import karrio.server.providers.models as providers
import karrio.server.serializers as serializers
import karrio.server.graph.utils as utils


@strawberry.input
class LogFilter(utils.Paginated):
    api_endpoint: typing.Optional[str] = strawberry.UNSET
    date_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    date_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    entity_id: typing.Optional[str] = strawberry.UNSET
    method: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[str] = strawberry.UNSET
    status_code: typing.Optional[typing.List[int]] = strawberry.UNSET


@strawberry.input
class TracingRecordFilter(utils.Paginated):
    key: typing.Optional[str] = strawberry.UNSET
    request_log_id: typing.Optional[int] = strawberry.UNSET
    date_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    date_before: typing.Optional[datetime.datetime] = strawberry.UNSET


@strawberry.input
class TrackerFilter(utils.Paginated):
    tracking_number: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[typing.List[str]] = strawberry.UNSET
    test_mode: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class ShipmentFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    address: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    reference: typing.Optional[str] = strawberry.UNSET
    service: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[typing.List[utils.ShipmentStatusEnum]] = strawberry.UNSET
    option_key: typing.Optional[typing.List[str]] = strawberry.UNSET
    option_value: typing.Optional[str] = strawberry.UNSET
    metadata_key: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata_value: typing.Optional[str] = strawberry.UNSET
    test_mode: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class TemplateFilter(utils.Paginated):
    label: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class AddressFilter(TemplateFilter):
    address: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class UpdateUserInput(utils.BaseInput):
    full_name: typing.Optional[str] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class TokenMutationInput(utils.BaseInput):
    password: typing.Optional[str] = strawberry.UNSET
    refresh: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class RequestEmailChangeMutationInput(utils.BaseInput):
    email: str
    password: str
    redirect_url: str


@strawberry.input
class ConfirmEmailChangeMutationInput(utils.BaseInput):
    token: str


@strawberry.input
class RegisterUserMutationInput(utils.BaseInput):
    email: str
    password1: str
    password2: str
    redirect_url: str
    full_name: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class ConfirmEmailMutationInput(utils.BaseInput):
    token: str


@strawberry.input
class ChangePasswordMutationInput(utils.BaseInput):
    old_password: str
    new_password1: str
    new_password2: str


@strawberry.input
class RequestPasswordResetMutationInput(utils.BaseInput):
    email: str
    redirect_url: str


@strawberry.input
class ConfirmPasswordResetMutationInput(utils.BaseInput):
    uid: str
    token: str
    new_password1: str
    new_password2: str


@strawberry.input
class EnableMultiFactorMutationInput(utils.BaseInput):
    password: str


@strawberry.input
class ConfirmMultiFactorMutationInput(utils.BaseInput):
    token: str


@strawberry.input
class DisableMultiFactorMutationInput(utils.BaseInput):
    password: str


@strawberry.input
class MetadataMutationInput(utils.BaseInput):
    id: str
    object_type: utils.MetadataObjectTypeEnum
    added_values: utils.JSON
    discarded_keys: typing.Optional[typing.List[str]]


@strawberry.input
class CommodityInput:
    weight: float
    weight_unit: utils.WeightUnitEnum
    quantity: typing.Optional[int] = 1
    sku: typing.Optional[str] = strawberry.UNSET
    hs_code: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    value_amount: typing.Optional[float] = strawberry.UNSET
    origin_country: typing.Optional[utils.CountryCodeEnum] = strawberry.UNSET
    value_currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    parent_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class UpdateCommodityInput(CommodityInput):
    id: typing.Optional[str] = strawberry.UNSET
    quantity: typing.Optional[int] = strawberry.UNSET
    weight: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET


@strawberry.input
class AddressInput:
    country_code: typing.Optional[utils.CountryCodeEnum]
    postal_code: typing.Optional[str] = strawberry.UNSET
    city: typing.Optional[str] = strawberry.UNSET
    federal_tax_id: typing.Optional[str] = strawberry.UNSET
    state_tax_id: typing.Optional[str] = strawberry.UNSET
    person_name: typing.Optional[str] = strawberry.UNSET
    company_name: typing.Optional[str] = strawberry.UNSET
    email: typing.Optional[str] = strawberry.UNSET
    phone_number: typing.Optional[str] = strawberry.UNSET
    state_code: typing.Optional[str] = strawberry.UNSET
    suburb: typing.Optional[str] = strawberry.UNSET
    residential: typing.Optional[bool] = strawberry.UNSET
    address_line1: typing.Optional[str] = strawberry.UNSET
    address_line2: typing.Optional[str] = strawberry.UNSET
    validate_location: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateAddressInput(AddressInput):
    id: typing.Optional[str] = strawberry.UNSET
    country_code: typing.Optional[utils.CountryCodeEnum] = strawberry.UNSET


@strawberry.input
class ParcelInput:
    weight: float
    weight_unit: utils.WeightUnitEnum
    width: typing.Optional[float] = strawberry.UNSET
    height: typing.Optional[float] = strawberry.UNSET
    length: typing.Optional[float] = strawberry.UNSET
    packaging_type: typing.Optional[str] = strawberry.UNSET
    package_preset: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    content: typing.Optional[str] = strawberry.UNSET
    is_document: typing.Optional[bool] = strawberry.UNSET
    dimension_unit: typing.Optional[utils.DimensionUnitEnum] = strawberry.UNSET
    reference_number: typing.Optional[str] = strawberry.UNSET
    freight_class: typing.Optional[str] = strawberry.UNSET
    items: typing.Optional[typing.List[CommodityInput]] = strawberry.UNSET


@strawberry.input
class UpdateParcelInput(ParcelInput):
    id: typing.Optional[str] = strawberry.UNSET
    weight: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET
    items: typing.Optional[typing.List[UpdateCommodityInput]] = strawberry.UNSET  # type: ignore


@strawberry.input
class DutyInput:
    paid_by: utils.PaidByEnum
    currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET
    account_number: typing.Optional[str] = strawberry.UNSET
    declared_value: typing.Optional[float] = strawberry.UNSET
    bill_to: typing.Optional[AddressInput] = strawberry.UNSET


@strawberry.input
class UpdateDutyInput(DutyInput):
    paid_by: typing.Optional[utils.PaidByEnum] = strawberry.UNSET


@strawberry.input
class CustomsInput:
    commodities: typing.List[CommodityInput]
    certify: typing.Optional[bool] = strawberry.UNSET
    commercial_invoice: typing.Optional[bool] = strawberry.UNSET
    content_type: typing.Optional[utils.CustomsContentTypeEnum] = strawberry.UNSET
    content_description: typing.Optional[str] = strawberry.UNSET
    incoterm: typing.Optional[utils.IncotermCodeEnum] = strawberry.UNSET
    invoice: typing.Optional[str] = strawberry.UNSET
    invoice_date: typing.Optional[datetime.date] = strawberry.UNSET
    signer: typing.Optional[str] = strawberry.UNSET
    duty: typing.Optional[DutyInput] = strawberry.UNSET
    duty_billing_address: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    options: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateCustomsInput(CustomsInput):
    id: typing.Optional[str] = strawberry.UNSET
    duty: typing.Optional[UpdateDutyInput] = strawberry.UNSET
    duty_billing_address: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    commodities: typing.Optional[typing.List[UpdateCommodityInput]] = strawberry.UNSET  # type: ignore


@strawberry.input
class PaymentInput:
    account_number: typing.Optional[str] = strawberry.UNSET
    paid_by: typing.Optional[utils.PaidByEnum] = strawberry.UNSET
    currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET


@strawberry.input
class PartialShipmentMutationInput(utils.BaseInput):
    id: str
    recipient: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    shipper: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    customs: typing.Optional[UpdateCustomsInput] = strawberry.UNSET
    parcels: typing.Optional[typing.List[UpdateParcelInput]] = strawberry.UNSET
    payment: typing.Optional[PaymentInput] = strawberry.UNSET
    billing_address: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    label_type: typing.Optional[utils.LabelTypeEnum] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    options: typing.Optional[utils.JSON] = strawberry.UNSET
    reference: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class ChangeShipmentStatusMutationInput(utils.BaseInput):
    id: str
    status: typing.Optional[utils.ManualShipmentStatusEnum]


@strawberry.input
class CreateAddressTemplateInput(utils.BaseInput):
    label: str
    address: AddressInput
    is_default: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateAddressTemplateInput(CreateAddressTemplateInput):
    id: str  # type: ignore
    label: typing.Optional[str]
    address: typing.Optional[UpdateAddressInput] = strawberry.UNSET


@strawberry.input
class CreateCustomsTemplateInput(utils.BaseInput):
    label: str
    customs: CustomsInput
    is_default: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateCustomsTemplateInput(CreateCustomsTemplateInput):
    id: str  # type: ignore
    label: typing.Optional[str] = strawberry.UNSET
    is_default: typing.Optional[bool] = strawberry.UNSET
    customs: typing.Optional[UpdateCustomsInput] = strawberry.UNSET  # type: ignore


@strawberry.input
class CreateParcelTemplateInput(utils.BaseInput):
    label: str
    parcel: ParcelInput
    is_default: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateParcelTemplateInput(CreateParcelTemplateInput):
    id: str  # type: ignore
    label: typing.Optional[str] = strawberry.UNSET
    is_default: typing.Optional[bool] = strawberry.UNSET
    parcel: typing.Optional[UpdateParcelInput] = strawberry.UNSET


@strawberry.input
class DeleteMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class LabelTemplateInput(utils.BaseInput):
    slug: str
    template: str
    template_type: utils.LabelTemplateTypeEnum
    width: typing.Optional[int] = strawberry.UNSET
    height: typing.Optional[int] = strawberry.UNSET
    shipment_sample: typing.Optional[utils.JSON] = strawberry.UNSET
    id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class CreateServiceLevelInput(utils.BaseInput):
    service_name: str
    service_code: str
    cost: float
    currency: utils.CurrencyCodeEnum

    description: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET

    estimated_transit_days: typing.Optional[int] = strawberry.UNSET

    max_weight: typing.Optional[float] = strawberry.UNSET
    max_width: typing.Optional[float] = strawberry.UNSET
    max_height: typing.Optional[float] = strawberry.UNSET
    max_length: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET
    dimension_unit: typing.Optional[utils.DimensionUnitEnum] = strawberry.UNSET

    domicile: typing.Optional[bool] = strawberry.UNSET
    international: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateServiceLevelInput(CreateServiceLevelInput):
    id: typing.Optional[str] = strawberry.UNSET
    service_name: typing.Optional[str] = strawberry.UNSET
    service_code: typing.Optional[str] = strawberry.UNSET
    cost: typing.Optional[float] = strawberry.UNSET
    currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET


def carrier_settings_inputs(is_update: bool = False) -> typing.Dict[str, typing.Type]:
    def carrier_settings_input(name: str, model):
        _name = f"{'Update' if is_update else ''}{model.__name__}Input"
        _RawSettings = pydoc.locate(f"karrio.mappers.{name}.Settings")
        _excluded = ["services", "id"]
        _optionals = ["account_country_code", "label_template", "test_mode"]
        _template_type: typing.Any = "LabelTemplateInput"
        _service_type: typing.Any = typing.List[  # type: ignore
            "UpdateServiceLevelInput" if is_update else "CreateServiceLevelInput"
        ]

        @strawberry.input
        class _CarrierInput(utils.BaseInput):
            if is_update:
                id: str

            if hasattr(model, "account_country_code"):
                account_country_code: typing.Optional[str] = strawberry.UNSET

            if hasattr(model, "label_template"):
                label_template: typing.Optional[_template_type] = strawberry.UNSET

            if hasattr(model, "services"):
                services: typing.Optional[_service_type] = strawberry.UNSET

            active: typing.Optional[bool] = True
            metadata: typing.Optional[utils.JSON] = strawberry.UNSET

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
                        if hasattr(model, k)
                    },
                    "__annotations__": {
                        k: (
                            typing.Optional[v]
                            if (
                                is_update
                                or k in _optionals
                                or serializers.is_field_optional(model, k)
                            )
                            else v
                        )
                        for k, v in annotations.items()
                        if k not in _excluded and hasattr(model, k)
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
        (utils.BaseInput,),
        {
            **{name: strawberry.UNSET for name in CreateCarrierInputs.keys()},
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
        (utils.BaseInput,),
        {
            **{name: strawberry.UNSET for name in UpdateCarrierInputs.keys()},
            "__annotations__": {
                name: typing.Optional[type]  # type:ignore
                for name, type in UpdateCarrierInputs.items()
            },
        },
    )
)


@strawberry.input
class SystemCarrierMutationInput(utils.BaseInput):
    id: str
    enable: bool
