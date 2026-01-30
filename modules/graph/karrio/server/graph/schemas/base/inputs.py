import pydoc
import typing
import datetime
import strawberry

import karrio.server.providers.models as providers
import karrio.server.serializers as serializers
import karrio.server.graph.utils as utils


@strawberry.input
class LogFilter(utils.Paginated):
    query: typing.Optional[str] = strawberry.UNSET
    api_endpoint: typing.Optional[str] = strawberry.UNSET
    remote_addr: typing.Optional[str] = strawberry.UNSET
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
    created_after: typing.Optional[str] = strawberry.UNSET
    created_before: typing.Optional[str] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class ShipmentFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    address: typing.Optional[str] = strawberry.UNSET
    id: typing.Optional[typing.List[str]] = strawberry.UNSET
    created_after: typing.Optional[str] = strawberry.UNSET
    created_before: typing.Optional[str] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    reference: typing.Optional[str] = strawberry.UNSET
    service: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[typing.List[utils.ShipmentStatusEnum]] = strawberry.UNSET
    option_key: typing.Optional[str] = strawberry.UNSET
    option_value: typing.Optional[utils.JSON] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[utils.JSON] = strawberry.UNSET
    meta_key: typing.Optional[str] = strawberry.UNSET
    meta_value: typing.Optional[utils.JSON] = strawberry.UNSET
    has_tracker: typing.Optional[bool] = strawberry.UNSET
    has_manifest: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class ManifestFilter(utils.Paginated):
    id: typing.Optional[typing.List[str]] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class PickupFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    id: typing.Optional[typing.List[str]] = strawberry.UNSET
    confirmation_number: typing.Optional[str] = strawberry.UNSET
    pickup_date_after: typing.Optional[str] = strawberry.UNSET
    pickup_date_before: typing.Optional[str] = strawberry.UNSET
    created_after: typing.Optional[datetime.datetime] = strawberry.UNSET
    created_before: typing.Optional[datetime.datetime] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET
    address: typing.Optional[str] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[str] = strawberry.UNSET
    meta_key: typing.Optional[str] = strawberry.UNSET
    meta_value: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class TemplateFilter(utils.Paginated):
    label: typing.Optional[str] = strawberry.UNSET
    keyword: typing.Optional[str] = strawberry.UNSET
    usage: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class AddressFilter(TemplateFilter):
    address: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class ProductFilter(TemplateFilter):
    sku: typing.Optional[str] = strawberry.UNSET
    origin_country: typing.Optional[utils.CountryCodeEnum] = strawberry.UNSET


@strawberry.input
class CarrierFilter(utils.Paginated):
    active: typing.Optional[bool] = strawberry.UNSET
    metadata_key: typing.Optional[str] = strawberry.UNSET
    metadata_value: typing.Optional[str] = strawberry.UNSET
    carrier_name: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class UpdateUserInput(utils.BaseInput):
    full_name: typing.Optional[str] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class WorkspaceConfigMutationInput(utils.BaseInput):
    # General preferences
    default_currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET
    default_country_code: typing.Optional[utils.CountryCodeEnum] = strawberry.UNSET
    default_label_type: typing.Optional[utils.LabelTypeEnum] = strawberry.UNSET

    default_weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET
    default_dimension_unit: typing.Optional[utils.DimensionUnitEnum] = strawberry.UNSET

    # Customs identifiers
    state_tax_id: typing.Optional[str] = strawberry.UNSET
    federal_tax_id: typing.Optional[str] = strawberry.UNSET

    customs_aes: typing.Optional[str] = strawberry.UNSET
    customs_eel_pfc: typing.Optional[str] = strawberry.UNSET
    customs_eori_number: typing.Optional[str] = strawberry.UNSET
    customs_license_number: typing.Optional[str] = strawberry.UNSET
    customs_certificate_number: typing.Optional[str] = strawberry.UNSET
    customs_nip_number: typing.Optional[str] = strawberry.UNSET
    customs_vat_registration_number: typing.Optional[str] = strawberry.UNSET

    # Default options
    insured_by_default: typing.Optional[bool] = strawberry.UNSET

    # Label printing
    label_message_1: typing.Optional[str] = strawberry.UNSET
    label_message_2: typing.Optional[str] = strawberry.UNSET
    label_message_3: typing.Optional[str] = strawberry.UNSET
    label_logo: typing.Optional[str] = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Labels (format uses default_label_type above)
    # ─────────────────────────────────────────────────────────────────
    print_label_size: typing.Optional[utils.LabelSizeEnum] = strawberry.UNSET
    print_label_show_options: typing.Optional[bool] = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Return Labels
    # ─────────────────────────────────────────────────────────────────
    print_return_label_size: typing.Optional[utils.LabelSizeEnum] = strawberry.UNSET
    print_return_label_show_options: typing.Optional[bool] = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Customs Documents
    # ─────────────────────────────────────────────────────────────────
    print_customs_size: typing.Optional[utils.LabelSizeEnum] = strawberry.UNSET
    print_customs_show_options: typing.Optional[bool] = strawberry.UNSET
    print_customs_with_label: typing.Optional[bool] = strawberry.UNSET
    print_customs_copies: typing.Optional[int] = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Settings
    # ─────────────────────────────────────────────────────────────────
    default_parcel_weight: typing.Optional[float] = strawberry.UNSET
    default_shipping_service: typing.Optional[str] = strawberry.UNSET
    default_shipping_carrier: typing.Optional[str] = strawberry.UNSET
    default_export_reason: typing.Optional[utils.ExportReasonEnum] = strawberry.UNSET
    default_delivery_instructions: typing.Optional[str] = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Label Options
    # ─────────────────────────────────────────────────────────────────
    label_show_postage_paid_logo: typing.Optional[bool] = strawberry.UNSET
    label_show_qr_code: typing.Optional[bool] = strawberry.UNSET
    customs_use_order_as_invoice: typing.Optional[bool] = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Recommendations Preferences
    # ─────────────────────────────────────────────────────────────────
    pref_first_mile: typing.Optional[typing.List[utils.FirstMileEnum]] = strawberry.UNSET
    pref_last_mile: typing.Optional[typing.List[utils.LastMileEnum]] = strawberry.UNSET
    pref_form_factor: typing.Optional[typing.List[utils.FormFactorEnum]] = strawberry.UNSET
    pref_age_check: typing.Optional[utils.AgeCheckEnum] = strawberry.UNSET
    pref_signature_required: typing.Optional[bool] = strawberry.UNSET
    pref_max_lead_time_days: typing.Optional[int] = strawberry.UNSET


@strawberry.input
class TokenMutationInput(utils.BaseInput):
    key: str
    password: typing.Optional[str] = strawberry.UNSET
    refresh: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class CreateAPIKeyMutationInput(utils.BaseInput):
    password: str
    label: str
    permissions: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class DeleteAPIKeyMutationInput(utils.BaseInput):
    password: str
    key: str


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
    title: typing.Optional[str] = strawberry.UNSET
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
    residential: typing.Optional[bool] = strawberry.UNSET
    street_number: typing.Optional[str] = strawberry.UNSET
    address_line1: typing.Optional[str] = strawberry.UNSET
    address_line2: typing.Optional[str] = strawberry.UNSET
    validate_location: typing.Optional[bool] = strawberry.UNSET


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
class PaymentInput:
    account_number: typing.Optional[str] = strawberry.UNSET
    paid_by: typing.Optional[utils.PaidByEnum] = strawberry.UNSET
    currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# ADDRESS TEMPLATE INPUTS (flat structure with meta as JSON for extensibility)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class CreateAddressInput(utils.BaseInput):
    """Flat address template input with meta for template metadata."""

    meta: utils.JSON
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
    residential: typing.Optional[bool] = strawberry.UNSET
    street_number: typing.Optional[str] = strawberry.UNSET
    address_line1: typing.Optional[str] = strawberry.UNSET
    address_line2: typing.Optional[str] = strawberry.UNSET
    validate_location: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateAddressInput(utils.BaseInput):
    """Flat address template update input."""

    id: str
    meta: typing.Optional[utils.JSON] = strawberry.UNSET
    country_code: typing.Optional[utils.CountryCodeEnum] = strawberry.UNSET
    postal_code: typing.Optional[str] = strawberry.UNSET
    city: typing.Optional[str] = strawberry.UNSET
    federal_tax_id: typing.Optional[str] = strawberry.UNSET
    state_tax_id: typing.Optional[str] = strawberry.UNSET
    person_name: typing.Optional[str] = strawberry.UNSET
    company_name: typing.Optional[str] = strawberry.UNSET
    email: typing.Optional[str] = strawberry.UNSET
    phone_number: typing.Optional[str] = strawberry.UNSET
    state_code: typing.Optional[str] = strawberry.UNSET
    residential: typing.Optional[bool] = strawberry.UNSET
    street_number: typing.Optional[str] = strawberry.UNSET
    address_line1: typing.Optional[str] = strawberry.UNSET
    address_line2: typing.Optional[str] = strawberry.UNSET
    validate_location: typing.Optional[bool] = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# PARCEL TEMPLATE INPUTS (flat structure with meta)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class CreateParcelInput(utils.BaseInput):
    """Flat parcel template input with meta for template metadata."""

    meta: utils.JSON
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
class UpdateParcelInput(utils.BaseInput):
    """Flat parcel template update input."""

    id: str
    meta: typing.Optional[utils.JSON] = strawberry.UNSET
    weight: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET
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
    items: typing.Optional[typing.List[UpdateCommodityInput]] = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# SHIPMENT MUTATION INPUTS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class PartialShipmentMutationInput(utils.BaseInput):
    id: str
    recipient: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    shipper: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    return_address: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    billing_address: typing.Optional[UpdateAddressInput] = strawberry.UNSET
    customs: typing.Optional[utils.JSON] = strawberry.UNSET
    parcels: typing.Optional[typing.List[UpdateParcelInput]] = strawberry.UNSET
    payment: typing.Optional[PaymentInput] = strawberry.UNSET
    label_type: typing.Optional[utils.LabelTypeEnum] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    options: typing.Optional[utils.JSON] = strawberry.UNSET
    reference: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class ChangeShipmentStatusMutationInput(utils.BaseInput):
    id: str
    status: typing.Optional[utils.ManualShipmentStatusEnum]


# ─────────────────────────────────────────────────────────────────────────────
# PRODUCT TEMPLATE INPUTS (flat structure with meta)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class CreateProductInput(utils.BaseInput):
    """Flat product template input with meta for template metadata."""

    meta: utils.JSON
    weight: float
    weight_unit: utils.WeightUnitEnum
    quantity: typing.Optional[int] = 1
    sku: typing.Optional[str] = strawberry.UNSET
    title: typing.Optional[str] = strawberry.UNSET
    hs_code: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    value_amount: typing.Optional[float] = strawberry.UNSET
    value_currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET
    origin_country: typing.Optional[utils.CountryCodeEnum] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateProductInput(utils.BaseInput):
    """Flat product template update input."""

    id: str
    meta: typing.Optional[utils.JSON] = strawberry.UNSET
    weight: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET
    quantity: typing.Optional[int] = strawberry.UNSET
    sku: typing.Optional[str] = strawberry.UNSET
    title: typing.Optional[str] = strawberry.UNSET
    hs_code: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    value_amount: typing.Optional[float] = strawberry.UNSET
    value_currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET
    origin_country: typing.Optional[utils.CountryCodeEnum] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


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
class ServiceLevelFeaturesInput(utils.BaseInput):
    """Structured service level features input.

    Defines the capabilities and characteristics of a shipping service.
    Used for filtering, display, and setting default options.
    """

    # First Mile: How parcels get to the carrier
    # "pick_up" | "drop_off" | "pick_up_and_drop_off"
    first_mile: typing.Optional[str] = strawberry.UNSET

    # Last Mile: How parcels are delivered to recipient
    # "home_delivery" | "service_point" | "mailbox"
    last_mile: typing.Optional[str] = strawberry.UNSET

    # Form Factor: Type of package the service supports
    # "letter" | "parcel" | "mailbox" | "pallet"
    form_factor: typing.Optional[str] = strawberry.UNSET

    # Type of Shipments: Business model support
    b2c: typing.Optional[bool] = strawberry.UNSET  # Business to Consumer
    b2b: typing.Optional[bool] = strawberry.UNSET  # Business to Business

    # Shipment Direction: "outbound" | "returns" | "both"
    shipment_type: typing.Optional[str] = strawberry.UNSET

    # Age Verification: null | "16" | "18"
    age_check: typing.Optional[str] = strawberry.UNSET

    # Default signature requirement
    signature: typing.Optional[bool] = strawberry.UNSET

    # Tracking availability
    tracked: typing.Optional[bool] = strawberry.UNSET

    # Insurance availability
    insurance: typing.Optional[bool] = strawberry.UNSET

    # Express/Priority service
    express: typing.Optional[bool] = strawberry.UNSET

    # Dangerous goods support
    dangerous_goods: typing.Optional[bool] = strawberry.UNSET

    # Weekend delivery options
    saturday_delivery: typing.Optional[bool] = strawberry.UNSET
    sunday_delivery: typing.Optional[bool] = strawberry.UNSET

    # Multi-package shipment support
    multicollo: typing.Optional[bool] = strawberry.UNSET

    # Neighbor delivery allowed
    neighbor_delivery: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class CreateServiceLevelInput(utils.BaseInput):
    """Input for creating a new service level."""

    service_name: str
    service_code: str
    currency: utils.CurrencyCodeEnum

    carrier_service_code: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET

    transit_days: typing.Optional[int] = strawberry.UNSET
    transit_time: typing.Optional[float] = strawberry.UNSET

    max_width: typing.Optional[float] = strawberry.UNSET
    max_height: typing.Optional[float] = strawberry.UNSET
    max_length: typing.Optional[float] = strawberry.UNSET
    dimension_unit: typing.Optional[utils.DimensionUnitEnum] = strawberry.UNSET

    min_weight: typing.Optional[float] = strawberry.UNSET
    max_weight: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET
    max_volume: typing.Optional[float] = strawberry.UNSET
    cost: typing.Optional[float] = strawberry.UNSET

    # Volumetric weight fields
    dim_factor: typing.Optional[float] = strawberry.UNSET
    use_volumetric: typing.Optional[bool] = strawberry.UNSET

    domicile: typing.Optional[bool] = strawberry.UNSET
    international: typing.Optional[bool] = strawberry.UNSET

    # Service features as structured object
    features: typing.Optional[ServiceLevelFeaturesInput] = strawberry.UNSET

    zone_ids: typing.Optional[typing.List[str]] = strawberry.UNSET
    surcharge_ids: typing.Optional[typing.List[str]] = strawberry.UNSET

    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateServiceLevelInput(utils.BaseInput):
    """Input for updating a service level."""

    id: typing.Optional[str] = strawberry.UNSET
    service_name: typing.Optional[str] = strawberry.UNSET
    service_code: typing.Optional[str] = strawberry.UNSET
    currency: typing.Optional[utils.CurrencyCodeEnum] = strawberry.UNSET

    carrier_service_code: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET

    transit_days: typing.Optional[int] = strawberry.UNSET
    transit_time: typing.Optional[float] = strawberry.UNSET

    max_width: typing.Optional[float] = strawberry.UNSET
    max_height: typing.Optional[float] = strawberry.UNSET
    max_length: typing.Optional[float] = strawberry.UNSET
    dimension_unit: typing.Optional[utils.DimensionUnitEnum] = strawberry.UNSET

    min_weight: typing.Optional[float] = strawberry.UNSET
    max_weight: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET
    max_volume: typing.Optional[float] = strawberry.UNSET
    cost: typing.Optional[float] = strawberry.UNSET

    # Volumetric weight fields
    dim_factor: typing.Optional[float] = strawberry.UNSET
    use_volumetric: typing.Optional[bool] = strawberry.UNSET

    domicile: typing.Optional[bool] = strawberry.UNSET
    international: typing.Optional[bool] = strawberry.UNSET

    # Service features as structured object
    features: typing.Optional[ServiceLevelFeaturesInput] = strawberry.UNSET

    zone_ids: typing.Optional[typing.List[str]] = strawberry.UNSET
    surcharge_ids: typing.Optional[typing.List[str]] = strawberry.UNSET

    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class CreateRateSheetMutationInput(utils.BaseInput):
    name: str
    carrier_name: utils.CarrierNameEnum
    services: typing.Optional[typing.List[CreateServiceLevelInput]] = strawberry.UNSET
    zones: typing.Optional[typing.List["SharedZoneInput"]] = strawberry.UNSET
    surcharges: typing.Optional[typing.List["SharedSurchargeInput"]] = strawberry.UNSET
    service_rates: typing.Optional[typing.List["ServiceRateInput"]] = strawberry.UNSET
    carriers: typing.Optional[typing.List[str]] = strawberry.UNSET
    origin_countries: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateRateSheetMutationInput(utils.BaseInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    services: typing.Optional[typing.List[UpdateServiceLevelInput]] = strawberry.UNSET
    zones: typing.Optional[typing.List["SharedZoneInput"]] = strawberry.UNSET
    surcharges: typing.Optional[typing.List["SharedSurchargeInput"]] = strawberry.UNSET
    service_rates: typing.Optional[typing.List["ServiceRateInput"]] = strawberry.UNSET
    carriers: typing.Optional[typing.List[str]] = strawberry.UNSET
    origin_countries: typing.Optional[typing.List[str]] = strawberry.UNSET
    remove_missing_services: typing.Optional[bool] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class DeleteRateSheetServiceMutationInput(utils.BaseInput):
    rate_sheet_id: str
    service_id: str


@strawberry.input
class RateSheetFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class CreateCarrierConnectionMutationInput(utils.BaseInput):
    carrier_name: utils.CarrierNameEnum
    carrier_id: str
    credentials: utils.JSON
    active: typing.Optional[bool] = True
    config: typing.Optional[utils.JSON] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    capabilities: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class UpdateCarrierConnectionMutationInput(utils.BaseInput):
    id: str
    active: typing.Optional[bool] = True
    carrier_id: typing.Optional[str] = strawberry.UNSET
    credentials: typing.Optional[utils.JSON] = strawberry.UNSET
    config: typing.Optional[utils.JSON] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    capabilities: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class SystemCarrierMutationInput(utils.BaseInput):
    id: str
    enable: typing.Optional[bool] = strawberry.UNSET
    config: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class CreateMetafieldInput(utils.BaseInput):
    key: str
    type: utils.MetafieldTypeEnum
    value: typing.Optional[utils.JSON] = strawberry.UNSET
    is_required: typing.Optional[bool] = strawberry.UNSET
    object_type: typing.Optional[str] = strawberry.UNSET
    object_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class UpdateMetafieldInput(CreateMetafieldInput):
    id: str
    key: typing.Optional[str] = strawberry.UNSET
    type: typing.Optional[utils.MetafieldTypeEnum] = strawberry.UNSET


@strawberry.input
class MetafieldInput(utils.BaseInput):
    key: str
    type: utils.MetafieldTypeEnum
    value: typing.Optional[utils.JSON] = strawberry.UNSET
    is_required: typing.Optional[bool] = strawberry.UNSET
    id: typing.Optional[str] = strawberry.UNSET
    object_type: typing.Optional[str] = strawberry.UNSET
    object_id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class MetafieldFilter(utils.Paginated):
    key: typing.Optional[str] = strawberry.UNSET
    type: typing.Optional[utils.MetafieldTypeEnum] = strawberry.UNSET
    is_required: typing.Optional[bool] = strawberry.UNSET
    object_type: typing.Optional[str] = strawberry.UNSET
    object_id: typing.Optional[str] = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# SHARED ZONE INPUTS (Rate Sheet Level)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class SharedZoneInput(utils.BaseInput):
    """Input for creating/updating a shared zone at the RateSheet level."""

    label: str
    id: typing.Optional[str] = strawberry.UNSET
    country_codes: typing.Optional[typing.List[str]] = strawberry.UNSET
    postal_codes: typing.Optional[typing.List[str]] = strawberry.UNSET
    cities: typing.Optional[typing.List[str]] = strawberry.UNSET
    transit_days: typing.Optional[int] = strawberry.UNSET
    transit_time: typing.Optional[float] = strawberry.UNSET
    radius: typing.Optional[float] = strawberry.UNSET
    latitude: typing.Optional[float] = strawberry.UNSET
    longitude: typing.Optional[float] = strawberry.UNSET
    # Weight constraints for this zone
    min_weight: typing.Optional[float] = strawberry.UNSET
    max_weight: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET


@strawberry.input
class AddSharedZoneMutationInput(utils.BaseInput):
    """Add a new shared zone to a rate sheet."""

    rate_sheet_id: str
    zone: SharedZoneInput


@strawberry.input
class UpdateSharedZoneMutationInput(utils.BaseInput):
    """Update a shared zone in a rate sheet."""

    rate_sheet_id: str
    zone_id: str
    zone: SharedZoneInput


@strawberry.input
class DeleteSharedZoneMutationInput(utils.BaseInput):
    """Delete a shared zone from a rate sheet."""

    rate_sheet_id: str
    zone_id: str


# ─────────────────────────────────────────────────────────────────────────────
# SHARED SURCHARGE INPUTS (Rate Sheet Level)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class SharedSurchargeInput(utils.BaseInput):
    """Input for creating/updating a shared surcharge at the RateSheet level."""

    name: str
    amount: float
    id: typing.Optional[str] = strawberry.UNSET
    surcharge_type: typing.Optional[str] = "fixed"  # "fixed" or "percentage"
    cost: typing.Optional[float] = strawberry.UNSET  # COGS
    active: typing.Optional[bool] = True


@strawberry.input
class AddSharedSurchargeMutationInput(utils.BaseInput):
    """Add a new shared surcharge to a rate sheet."""

    rate_sheet_id: str
    surcharge: SharedSurchargeInput


@strawberry.input
class UpdateSharedSurchargeMutationInput(utils.BaseInput):
    """Update a shared surcharge in a rate sheet."""

    rate_sheet_id: str
    surcharge_id: str
    surcharge: SharedSurchargeInput


@strawberry.input
class DeleteSharedSurchargeMutationInput(utils.BaseInput):
    """Delete a shared surcharge from a rate sheet."""

    rate_sheet_id: str
    surcharge_id: str


@strawberry.input
class BatchUpdateSurchargesMutationInput(utils.BaseInput):
    """Batch update multiple surcharges in a rate sheet."""

    rate_sheet_id: str
    surcharges: typing.List[SharedSurchargeInput]


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE RATE INPUTS (Service-Zone Rate Mapping)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class ServiceRateInput(utils.BaseInput):
    """Input for a service-zone rate mapping."""

    service_id: str
    zone_id: str
    rate: float
    cost: typing.Optional[float] = strawberry.UNSET  # COGS
    min_weight: typing.Optional[float] = strawberry.UNSET
    max_weight: typing.Optional[float] = strawberry.UNSET
    transit_days: typing.Optional[int] = strawberry.UNSET
    transit_time: typing.Optional[float] = strawberry.UNSET


@strawberry.input
class UpdateServiceRateMutationInput(utils.BaseInput):
    """Update a single service-zone rate."""

    rate_sheet_id: str
    service_id: str
    zone_id: str
    rate: float
    cost: typing.Optional[float] = strawberry.UNSET
    min_weight: typing.Optional[float] = strawberry.UNSET
    max_weight: typing.Optional[float] = strawberry.UNSET
    transit_days: typing.Optional[int] = strawberry.UNSET
    transit_time: typing.Optional[float] = strawberry.UNSET


@strawberry.input
class BatchUpdateServiceRatesMutationInput(utils.BaseInput):
    """Batch update multiple service-zone rates."""

    rate_sheet_id: str
    rates: typing.List[ServiceRateInput]


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE ZONE/SURCHARGE ASSIGNMENT INPUTS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class UpdateServiceZoneIdsMutationInput(utils.BaseInput):
    """Update zone_ids for a service level."""

    rate_sheet_id: str
    service_id: str
    zone_ids: typing.List[str]


@strawberry.input
class UpdateServiceSurchargeIdsMutationInput(utils.BaseInput):
    """Update surcharge_ids for a service level."""

    rate_sheet_id: str
    service_id: str
    surcharge_ids: typing.List[str]
