import pydoc
import typing
import datetime
import strawberry

import karrio.server.providers.models as providers
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
    request_log_id: typing.Optional[str] = strawberry.UNSET
    date_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    date_before: typing.Optional[datetime.datetime] = strawberry.UNSET


@strawberry.input
class TrackerFilter(utils.Paginated):
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[typing.List[str]] = strawberry.UNSET
    test_mode: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class ShipmentFilter(utils.Paginated):
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
    full_name: typing.Optional[str] = None


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
    uuid: str
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
    object_type: utils.MetadataObjectTypeEnum  # type:ignore
    added_values: "utils.JSON"  # type:ignore
    delete_keys: typing.Optional[typing.List[str]]


@strawberry.input
class CommodityInput:
    sku: typing.Optional[str]
    quantity: typing.Optional[int]
    weight: typing.Optional[float]
    description: typing.Optional[str]
    value_amount: typing.Optional[float]
    weight_unit: typing.Optional[utils.WeightUnitEnum]
    origin_country: typing.Optional[utils.CountryCodeEnum]
    value_currency: typing.Optional[utils.CurrencyCodeEnum]
    metadata: typing.Optional[utils.JSON]
    parent_id: typing.Optional[str]


@strawberry.input
class AddressInput:
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
    weight_unit: typing.Optional[utils.WeightUnitEnum]
    dimension_unit: typing.Optional[utils.DimensionUnitEnum]
    reference_number: typing.Optional[str]
    items: typing.Optional[typing.List[CommodityInput]]


@strawberry.input
class DutyInput:
    paid_by: typing.Optional[utils.PaidByEnum]
    currency: typing.Optional[utils.CountryCodeEnum]
    account_number: typing.Optional[str]
    declared_value: typing.Optional[float]
    bill_to: typing.Optional[AddressInput]


@strawberry.input
class CustomsInput:
    certify: typing.Optional[bool]
    commercial_invoice: typing.Optional[bool]
    content_type: typing.Optional[utils.CustomsContentTypeEnum]
    content_description: typing.Optional[str]
    incoterm: typing.Optional[utils.IncotermCodeEnum]
    invoice: typing.Optional[str]
    invoice_date: typing.Optional[datetime.date]
    signer: typing.Optional[str]
    duty: typing.Optional[DutyInput]
    options: typing.Optional[utils.JSON]
    commodities: typing.Optional[typing.List[CommodityInput]]


@strawberry.input
class PaymentInput:
    account_number: typing.Optional[str]
    paid_by: typing.Optional[utils.PaidByEnum]
    currency: typing.Optional[utils.CurrencyCodeEnum]


@strawberry.input
class PartialShipmentMutationInput(utils.BaseInput):
    id: str
    recipient: typing.Optional[AddressInput]
    shipper: typing.Optional[AddressInput]
    customs: typing.Optional[CustomsInput]
    parcels: typing.Optional[typing.List[ParcelInput]]
    payment: typing.Optional[PaymentInput]
    options: typing.Optional[utils.JSON]
    metadata: typing.Optional[utils.JSON]
    reference: typing.Optional[str]


@strawberry.input
class CreateAddressTemplateInput(utils.BaseInput):
    label: str
    address: AddressInput
    is_default: typing.Optional[bool]


@strawberry.input
class UpdateAddressTemplateInput(CreateAddressTemplateInput):
    id: str
    label: typing.Optional[str]
    address: typing.Optional[AddressInput]


@strawberry.input
class CreateCustomsTemplateInput(utils.BaseInput):
    label: str
    customs: CustomsInput
    is_default: typing.Optional[bool]


@strawberry.input
class UpdateCustomsTemplateInput(CreateCustomsTemplateInput):
    id: str
    label: typing.Optional[str]
    customs: typing.Optional[CustomsInput]


@strawberry.input
class CreateParcelTemplateInput(utils.BaseInput):
    label: str
    parcel: ParcelInput
    is_default: typing.Optional[bool]


@strawberry.input
class UpdateParcelTemplateInput(CreateParcelTemplateInput):
    id: str
    label: typing.Optional[str]
    parcel: typing.Optional[ParcelInput]


@strawberry.input
class DeleteMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class CreateLabelTemplateInput(utils.BaseInput):
    slug: str
    template: str
    template_type: utils.LabelTemplateTypeEnum
    width: typing.Optional[int]
    height: typing.Optional[int]
    shipment_sample: typing.Optional[utils.JSON]


@strawberry.input
class UpdateLabelTemplateInput(utils.BaseInput):
    id: str
    slug: typing.Optional[str]
    template: typing.Optional[str]
    template_type: typing.Optional[utils.LabelTemplateTypeEnum]


@strawberry.input
class CreateServiceLevelInput(utils.BaseInput):
    service_name: str
    service_code: str
    cost: float
    currency: utils.CurrencyCodeEnum

    description: typing.Optional[str]
    active: typing.Optional[bool]

    estimated_transit_days: typing.Optional[int]

    max_weight: typing.Optional[float]
    max_width: typing.Optional[float]
    max_height: typing.Optional[float]
    max_length: typing.Optional[float]
    weight_unit: typing.Optional[utils.WeightUnitEnum]
    dimension_unit: typing.Optional[utils.DimensionUnitEnum]

    domicile: typing.Optional[bool]
    international: typing.Optional[bool]


@strawberry.input
class UpdateServiceLevelInput(utils.BaseInput):
    id: str
    service_name: typing.Optional[str]
    service_code: typing.Optional[str]
    cost: typing.Optional[float]
    currency: typing.Optional[utils.CurrencyCodeEnum]


def carrier_settings_inputs(is_update: bool = False) -> typing.Dict[str, typing.Type]:
    def carrier_settings_input(name: str, model):
        _name = f"{'Update' if is_update else ''}{model.__name__}Input"
        _RawSettings = pydoc.locate(f"karrio.mappers.{name}.Settings")
        _excluded = ["services", "id"]
        _optionals = ["account_country_code", "label_template"]
        _template_type: typing.Any = (
            "UpdateLabelTemplateInput" if is_update else "CreateLabelTemplateInput"
        )
        _service_type: typing.Any = typing.List[ # type: ignore
            "UpdateServiceLevelInput" if is_update else "CreateServiceLevelInput"
        ]

        @strawberry.input
        class _CarrierInput(utils.BaseInput):
            if is_update:
                id: str = strawberry.UNSET

            if hasattr(model, "account_country_code"):
                account_country_code: typing.Optional[str] = strawberry.UNSET

            if hasattr(model, "label_template"):
                label_template: typing.Optional[_template_type] = strawberry.UNSET

            if hasattr(model, "services"):
                services: typing.Optional[_service_type] = strawberry.UNSET

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
        (utils.BaseInput,),
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
