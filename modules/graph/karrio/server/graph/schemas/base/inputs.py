import datetime

import karrio.server.graph.utils as utils
import strawberry


@strawberry.input
class LogFilter(utils.Paginated):
    query: str | None = strawberry.UNSET
    api_endpoint: str | None = strawberry.UNSET
    remote_addr: str | None = strawberry.UNSET
    date_after: datetime.datetime | None = strawberry.UNSET
    date_before: datetime.datetime | None = strawberry.UNSET
    entity_id: str | None = strawberry.UNSET
    method: list[str] | None = strawberry.UNSET
    status: str | None = strawberry.UNSET
    status_code: list[int] | None = strawberry.UNSET
    request_id: str | None = strawberry.UNSET


@strawberry.input
class TracingRecordFilter(utils.Paginated):
    key: str | None = strawberry.UNSET
    request_log_id: int | None = strawberry.UNSET
    date_after: datetime.datetime | None = strawberry.UNSET
    date_before: datetime.datetime | None = strawberry.UNSET
    keyword: str | None = strawberry.UNSET
    request_id: str | None = strawberry.UNSET


@strawberry.input
class TrackerFilter(utils.Paginated):
    tracking_number: str | None = strawberry.UNSET
    created_after: str | None = strawberry.UNSET
    created_before: str | None = strawberry.UNSET
    carrier_name: list[str] | None = strawberry.UNSET
    status: list[str] | None = strawberry.UNSET
    keyword: str | None = strawberry.UNSET
    request_id: str | None = strawberry.UNSET
    is_archived: bool | None = strawberry.UNSET


@strawberry.input
class ShipmentFilter(utils.Paginated):
    keyword: str | None = strawberry.UNSET
    address: str | None = strawberry.UNSET
    id: list[str] | None = strawberry.UNSET
    created_after: str | None = strawberry.UNSET
    created_before: str | None = strawberry.UNSET
    carrier_name: list[str] | None = strawberry.UNSET
    reference: str | None = strawberry.UNSET
    order_id: str | None = strawberry.UNSET
    service: list[str] | None = strawberry.UNSET
    status: list[utils.ShipmentStatusEnum] | None = strawberry.UNSET
    option_key: str | None = strawberry.UNSET
    option_value: utils.JSON | None = strawberry.UNSET
    metadata_key: str | None = strawberry.UNSET
    metadata_value: utils.JSON | None = strawberry.UNSET
    meta_key: str | None = strawberry.UNSET
    meta_value: utils.JSON | None = strawberry.UNSET
    has_tracker: bool | None = strawberry.UNSET
    has_manifest: bool | None = strawberry.UNSET
    is_return: bool | None = strawberry.UNSET
    request_id: str | None = strawberry.UNSET
    is_archived: bool | None = strawberry.UNSET


@strawberry.input
class ManifestFilter(utils.Paginated):
    id: list[str] | None = strawberry.UNSET
    created_after: datetime.datetime | None = strawberry.UNSET
    created_before: datetime.datetime | None = strawberry.UNSET
    carrier_name: list[str] | None = strawberry.UNSET
    request_id: str | None = strawberry.UNSET


@strawberry.input
class PickupFilter(utils.Paginated):
    keyword: str | None = strawberry.UNSET
    id: list[str] | None = strawberry.UNSET
    status: list[str] | None = strawberry.UNSET
    confirmation_number: str | None = strawberry.UNSET
    pickup_date_after: str | None = strawberry.UNSET
    pickup_date_before: str | None = strawberry.UNSET
    created_after: datetime.datetime | None = strawberry.UNSET
    created_before: datetime.datetime | None = strawberry.UNSET
    carrier_name: list[str] | None = strawberry.UNSET
    address: str | None = strawberry.UNSET
    metadata_key: str | None = strawberry.UNSET
    metadata_value: str | None = strawberry.UNSET
    meta_key: str | None = strawberry.UNSET
    meta_value: str | None = strawberry.UNSET
    request_id: str | None = strawberry.UNSET
    is_archived: bool | None = strawberry.UNSET


@strawberry.input
class TemplateFilter(utils.Paginated):
    label: str | None = strawberry.UNSET
    keyword: str | None = strawberry.UNSET
    usage: str | None = strawberry.UNSET


@strawberry.input
class AddressFilter(TemplateFilter):
    address: str | None = strawberry.UNSET


@strawberry.input
class ProductFilter(TemplateFilter):
    sku: str | None = strawberry.UNSET
    origin_country: utils.CountryCodeEnum | None = strawberry.UNSET


@strawberry.input
class CarrierFilter(utils.Paginated):
    active: bool | None = strawberry.UNSET
    metadata_key: str | None = strawberry.UNSET
    metadata_value: str | None = strawberry.UNSET
    carrier_name: list[str] | None = strawberry.UNSET


@strawberry.input
class UpdateUserInput(utils.BaseInput):
    full_name: str | None = strawberry.UNSET
    is_active: bool | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET


@strawberry.input
class WorkspaceConfigMutationInput(utils.BaseInput):
    # General preferences
    default_currency: utils.CurrencyCodeEnum | None = strawberry.UNSET
    default_country_code: utils.CountryCodeEnum | None = strawberry.UNSET
    default_label_type: utils.LabelTypeEnum | None = strawberry.UNSET

    default_weight_unit: utils.WeightUnitEnum | None = strawberry.UNSET
    default_dimension_unit: utils.DimensionUnitEnum | None = strawberry.UNSET

    # Customs identifiers
    state_tax_id: str | None = strawberry.UNSET
    federal_tax_id: str | None = strawberry.UNSET

    customs_aes: str | None = strawberry.UNSET
    customs_eel_pfc: str | None = strawberry.UNSET
    customs_eori_number: str | None = strawberry.UNSET
    customs_license_number: str | None = strawberry.UNSET
    customs_certificate_number: str | None = strawberry.UNSET
    customs_nip_number: str | None = strawberry.UNSET
    customs_vat_registration_number: str | None = strawberry.UNSET

    # Default options
    insured_by_default: bool | None = strawberry.UNSET

    # Label printing
    label_message_1: str | None = strawberry.UNSET
    label_message_2: str | None = strawberry.UNSET
    label_message_3: str | None = strawberry.UNSET
    label_logo: str | None = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Labels (format uses default_label_type above)
    # ─────────────────────────────────────────────────────────────────
    print_label_size: utils.LabelSizeEnum | None = strawberry.UNSET
    print_label_show_options: bool | None = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Return Labels
    # ─────────────────────────────────────────────────────────────────
    print_return_label_size: utils.LabelSizeEnum | None = strawberry.UNSET
    print_return_label_show_options: bool | None = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Printing Options - Customs Documents
    # ─────────────────────────────────────────────────────────────────
    print_customs_size: utils.LabelSizeEnum | None = strawberry.UNSET
    print_customs_show_options: bool | None = strawberry.UNSET
    print_customs_with_label: bool | None = strawberry.UNSET
    print_customs_copies: int | None = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Settings
    # ─────────────────────────────────────────────────────────────────
    default_parcel_weight: float | None = strawberry.UNSET
    default_shipping_service: str | None = strawberry.UNSET
    default_shipping_carrier: str | None = strawberry.UNSET
    default_export_reason: utils.ExportReasonEnum | None = strawberry.UNSET
    default_delivery_instructions: str | None = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Label Options
    # ─────────────────────────────────────────────────────────────────
    label_show_postage_paid_logo: bool | None = strawberry.UNSET
    label_show_qr_code: bool | None = strawberry.UNSET
    customs_use_order_as_invoice: bool | None = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Shipping Defaults - Recommendations Preferences
    # ─────────────────────────────────────────────────────────────────
    pref_first_mile: list[utils.FirstMileEnum] | None = strawberry.UNSET
    pref_last_mile: list[utils.LastMileEnum] | None = strawberry.UNSET
    pref_form_factor: list[utils.FormFactorEnum] | None = strawberry.UNSET
    pref_age_check: utils.AgeCheckEnum | None = strawberry.UNSET
    pref_signature_required: bool | None = strawberry.UNSET
    pref_max_lead_time_days: int | None = strawberry.UNSET

    # ─────────────────────────────────────────────────────────────────
    # Workspace Settings
    # ─────────────────────────────────────────────────────────────────
    shipping_app_test_mode: bool | None = strawberry.UNSET


@strawberry.input
class TokenMutationInput(utils.BaseInput):
    key: str
    password: str | None = strawberry.UNSET
    refresh: bool | None = strawberry.UNSET


@strawberry.input
class CreateAPIKeyMutationInput(utils.BaseInput):
    password: str
    label: str
    permissions: list[str] | None = strawberry.UNSET


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
    full_name: str | None = strawberry.UNSET


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
    discarded_keys: list[str] | None


@strawberry.input
class CommodityInput:
    weight: float
    weight_unit: utils.WeightUnitEnum
    quantity: int | None = 1
    sku: str | None = strawberry.UNSET
    title: str | None = strawberry.UNSET
    hs_code: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    value_amount: float | None = strawberry.UNSET
    origin_country: utils.CountryCodeEnum | None = strawberry.UNSET
    value_currency: utils.CurrencyCodeEnum | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    parent_id: str | None = strawberry.UNSET


@strawberry.input
class UpdateCommodityInput(CommodityInput):
    id: str | None = strawberry.UNSET
    quantity: int | None = strawberry.UNSET
    weight: float | None = strawberry.UNSET
    weight_unit: utils.WeightUnitEnum | None = strawberry.UNSET


@strawberry.input
class AddressInput:
    country_code: utils.CountryCodeEnum | None
    postal_code: str | None = strawberry.UNSET
    city: str | None = strawberry.UNSET
    federal_tax_id: str | None = strawberry.UNSET
    state_tax_id: str | None = strawberry.UNSET
    person_name: str | None = strawberry.UNSET
    company_name: str | None = strawberry.UNSET
    email: str | None = strawberry.UNSET
    phone_number: str | None = strawberry.UNSET
    state_code: str | None = strawberry.UNSET
    residential: bool | None = strawberry.UNSET
    street_number: str | None = strawberry.UNSET
    address_line1: str | None = strawberry.UNSET
    address_line2: str | None = strawberry.UNSET
    validate_location: bool | None = strawberry.UNSET


@strawberry.input
class ParcelInput:
    weight: float
    weight_unit: utils.WeightUnitEnum
    width: float | None = strawberry.UNSET
    height: float | None = strawberry.UNSET
    length: float | None = strawberry.UNSET
    packaging_type: str | None = strawberry.UNSET
    package_preset: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    content: str | None = strawberry.UNSET
    is_document: bool | None = strawberry.UNSET
    dimension_unit: utils.DimensionUnitEnum | None = strawberry.UNSET
    reference_number: str | None = strawberry.UNSET
    freight_class: str | None = strawberry.UNSET
    items: list[CommodityInput] | None = strawberry.UNSET


@strawberry.input
class DutyInput:
    paid_by: utils.PaidByEnum
    currency: utils.CurrencyCodeEnum | None = strawberry.UNSET
    account_number: str | None = strawberry.UNSET
    declared_value: float | None = strawberry.UNSET
    bill_to: AddressInput | None = strawberry.UNSET


@strawberry.input
class UpdateDutyInput(DutyInput):
    paid_by: utils.PaidByEnum | None = strawberry.UNSET


@strawberry.input
class PaymentInput:
    account_number: str | None = strawberry.UNSET
    paid_by: utils.PaidByEnum | None = strawberry.UNSET
    currency: utils.CurrencyCodeEnum | None = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# ADDRESS TEMPLATE INPUTS (flat structure with meta as JSON for extensibility)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class CreateAddressInput(utils.BaseInput):
    """Flat address template input with meta for template metadata."""

    meta: utils.JSON
    country_code: utils.CountryCodeEnum | None
    postal_code: str | None = strawberry.UNSET
    city: str | None = strawberry.UNSET
    federal_tax_id: str | None = strawberry.UNSET
    state_tax_id: str | None = strawberry.UNSET
    person_name: str | None = strawberry.UNSET
    company_name: str | None = strawberry.UNSET
    email: str | None = strawberry.UNSET
    phone_number: str | None = strawberry.UNSET
    state_code: str | None = strawberry.UNSET
    residential: bool | None = strawberry.UNSET
    street_number: str | None = strawberry.UNSET
    address_line1: str | None = strawberry.UNSET
    address_line2: str | None = strawberry.UNSET
    validate_location: bool | None = strawberry.UNSET


@strawberry.input
class UpdateAddressInput(utils.BaseInput):
    """Flat address template update input."""

    id: str
    meta: utils.JSON | None = strawberry.UNSET
    country_code: utils.CountryCodeEnum | None = strawberry.UNSET
    postal_code: str | None = strawberry.UNSET
    city: str | None = strawberry.UNSET
    federal_tax_id: str | None = strawberry.UNSET
    state_tax_id: str | None = strawberry.UNSET
    person_name: str | None = strawberry.UNSET
    company_name: str | None = strawberry.UNSET
    email: str | None = strawberry.UNSET
    phone_number: str | None = strawberry.UNSET
    state_code: str | None = strawberry.UNSET
    residential: bool | None = strawberry.UNSET
    street_number: str | None = strawberry.UNSET
    address_line1: str | None = strawberry.UNSET
    address_line2: str | None = strawberry.UNSET
    validate_location: bool | None = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# PARCEL TEMPLATE INPUTS (flat structure with meta)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class CreateParcelInput(utils.BaseInput):
    """Flat parcel template input with meta for template metadata."""

    meta: utils.JSON
    weight: float
    weight_unit: utils.WeightUnitEnum
    width: float | None = strawberry.UNSET
    height: float | None = strawberry.UNSET
    length: float | None = strawberry.UNSET
    packaging_type: str | None = strawberry.UNSET
    package_preset: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    content: str | None = strawberry.UNSET
    is_document: bool | None = strawberry.UNSET
    dimension_unit: utils.DimensionUnitEnum | None = strawberry.UNSET
    reference_number: str | None = strawberry.UNSET
    freight_class: str | None = strawberry.UNSET
    items: list[CommodityInput] | None = strawberry.UNSET


@strawberry.input
class UpdateParcelInput(utils.BaseInput):
    """Flat parcel template update input."""

    id: str
    meta: utils.JSON | None = strawberry.UNSET
    weight: float | None = strawberry.UNSET
    weight_unit: utils.WeightUnitEnum | None = strawberry.UNSET
    width: float | None = strawberry.UNSET
    height: float | None = strawberry.UNSET
    length: float | None = strawberry.UNSET
    packaging_type: str | None = strawberry.UNSET
    package_preset: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    content: str | None = strawberry.UNSET
    is_document: bool | None = strawberry.UNSET
    dimension_unit: utils.DimensionUnitEnum | None = strawberry.UNSET
    reference_number: str | None = strawberry.UNSET
    freight_class: str | None = strawberry.UNSET
    items: list[UpdateCommodityInput] | None = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# SHIPMENT MUTATION INPUTS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class PartialShipmentMutationInput(utils.BaseInput):
    id: str
    recipient: UpdateAddressInput | None = strawberry.UNSET
    shipper: UpdateAddressInput | None = strawberry.UNSET
    return_address: UpdateAddressInput | None = strawberry.UNSET
    billing_address: UpdateAddressInput | None = strawberry.UNSET
    customs: utils.JSON | None = strawberry.UNSET
    parcels: list[UpdateParcelInput] | None = strawberry.UNSET
    payment: PaymentInput | None = strawberry.UNSET
    label_type: utils.LabelTypeEnum | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    options: utils.JSON | None = strawberry.UNSET
    reference: str | None = strawberry.UNSET
    order_id: str | None = strawberry.UNSET


@strawberry.input
class ChangeShipmentStatusMutationInput(utils.BaseInput):
    id: str
    status: utils.ManualShipmentStatusEnum | None


# ─────────────────────────────────────────────────────────────────────────────
# PRODUCT TEMPLATE INPUTS (flat structure with meta)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class CreateProductInput(utils.BaseInput):
    """Flat product template input with meta for template metadata."""

    meta: utils.JSON
    weight: float
    weight_unit: utils.WeightUnitEnum
    quantity: int | None = 1
    sku: str | None = strawberry.UNSET
    title: str | None = strawberry.UNSET
    hs_code: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    value_amount: float | None = strawberry.UNSET
    value_currency: utils.CurrencyCodeEnum | None = strawberry.UNSET
    origin_country: utils.CountryCodeEnum | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET


@strawberry.input
class UpdateProductInput(utils.BaseInput):
    """Flat product template update input."""

    id: str
    meta: utils.JSON | None = strawberry.UNSET
    weight: float | None = strawberry.UNSET
    weight_unit: utils.WeightUnitEnum | None = strawberry.UNSET
    quantity: int | None = strawberry.UNSET
    sku: str | None = strawberry.UNSET
    title: str | None = strawberry.UNSET
    hs_code: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    value_amount: float | None = strawberry.UNSET
    value_currency: utils.CurrencyCodeEnum | None = strawberry.UNSET
    origin_country: utils.CountryCodeEnum | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET


@strawberry.input
class DeleteMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class LabelTemplateInput(utils.BaseInput):
    slug: str
    template: str
    template_type: utils.LabelTemplateTypeEnum
    width: int | None = strawberry.UNSET
    height: int | None = strawberry.UNSET
    shipment_sample: utils.JSON | None = strawberry.UNSET
    id: str | None = strawberry.UNSET


@strawberry.input
class ServiceLevelFeaturesInput(utils.BaseInput):
    """Structured service level features input.

    Defines the capabilities and characteristics of a shipping service.
    Used for filtering, display, and setting default options.
    """

    # First Mile: How parcels get to the carrier
    # "pick_up" | "drop_off" | "pick_up_and_drop_off"
    first_mile: str | None = strawberry.UNSET

    # Last Mile: How parcels are delivered to recipient
    # "home_delivery" | "service_point" | "mailbox"
    last_mile: str | None = strawberry.UNSET

    # Form Factor: Type of package the service supports
    # "letter" | "parcel" | "mailbox" | "pallet"
    form_factor: str | None = strawberry.UNSET

    # Type of Shipments: Business model support
    b2c: bool | None = strawberry.UNSET  # Business to Consumer
    b2b: bool | None = strawberry.UNSET  # Business to Business

    # Shipment Direction: "outbound" | "returns" | "both"
    shipment_type: str | None = strawberry.UNSET

    # Age Verification: null | "16" | "18"
    age_check: str | None = strawberry.UNSET

    # Default signature requirement
    signature: bool | None = strawberry.UNSET

    # Tracking availability
    tracked: bool | None = strawberry.UNSET

    # Insurance availability
    insurance: bool | None = strawberry.UNSET

    # Express/Priority service
    express: bool | None = strawberry.UNSET

    # Dangerous goods support
    dangerous_goods: bool | None = strawberry.UNSET

    # Weekend delivery options
    saturday_delivery: bool | None = strawberry.UNSET
    sunday_delivery: bool | None = strawberry.UNSET

    # Multi-package shipment support
    multicollo: bool | None = strawberry.UNSET

    # Neighbor delivery allowed
    neighbor_delivery: bool | None = strawberry.UNSET


@strawberry.input
class CreateServiceLevelInput(utils.BaseInput):
    """Input for creating a new service level."""

    service_name: str
    service_code: str
    currency: utils.CurrencyCodeEnum

    carrier_service_code: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    active: bool | None = strawberry.UNSET

    transit_days: int | None = strawberry.UNSET
    transit_time: float | None = strawberry.UNSET

    max_width: float | None = strawberry.UNSET
    max_height: float | None = strawberry.UNSET
    max_length: float | None = strawberry.UNSET
    dimension_unit: utils.DimensionUnitEnum | None = strawberry.UNSET

    min_weight: float | None = strawberry.UNSET
    max_weight: float | None = strawberry.UNSET
    weight_unit: utils.WeightUnitEnum | None = strawberry.UNSET
    max_volume: float | None = strawberry.UNSET
    cost: float | None = strawberry.UNSET

    # Volumetric weight fields
    dim_factor: float | None = strawberry.UNSET
    use_volumetric: bool | None = strawberry.UNSET

    domicile: bool | None = strawberry.UNSET
    international: bool | None = strawberry.UNSET

    # Service features as structured object
    features: ServiceLevelFeaturesInput | None = strawberry.UNSET

    # Backward-compat: allow feature fields at root level (merged into features)
    age_check: str | None = strawberry.UNSET
    neighbor_delivery: bool | None = strawberry.UNSET
    saturday_delivery: bool | None = strawberry.UNSET

    zone_ids: list[str] | None = strawberry.UNSET
    surcharge_ids: list[str] | None = strawberry.UNSET

    metadata: utils.JSON | None = strawberry.UNSET
    pricing_config: utils.JSON | None = strawberry.UNSET


@strawberry.input
class UpdateServiceLevelInput(utils.BaseInput):
    """Input for updating a service level."""

    id: str | None = strawberry.UNSET
    service_name: str | None = strawberry.UNSET
    service_code: str | None = strawberry.UNSET
    currency: utils.CurrencyCodeEnum | None = strawberry.UNSET

    carrier_service_code: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    active: bool | None = strawberry.UNSET

    transit_days: int | None = strawberry.UNSET
    transit_time: float | None = strawberry.UNSET

    max_width: float | None = strawberry.UNSET
    max_height: float | None = strawberry.UNSET
    max_length: float | None = strawberry.UNSET
    dimension_unit: utils.DimensionUnitEnum | None = strawberry.UNSET

    min_weight: float | None = strawberry.UNSET
    max_weight: float | None = strawberry.UNSET
    weight_unit: utils.WeightUnitEnum | None = strawberry.UNSET
    max_volume: float | None = strawberry.UNSET
    cost: float | None = strawberry.UNSET

    # Volumetric weight fields
    dim_factor: float | None = strawberry.UNSET
    use_volumetric: bool | None = strawberry.UNSET

    domicile: bool | None = strawberry.UNSET
    international: bool | None = strawberry.UNSET

    # Service features as structured object
    features: ServiceLevelFeaturesInput | None = strawberry.UNSET

    # Backward-compat: allow feature fields at root level (merged into features)
    age_check: str | None = strawberry.UNSET
    neighbor_delivery: bool | None = strawberry.UNSET
    saturday_delivery: bool | None = strawberry.UNSET

    zone_ids: list[str] | None = strawberry.UNSET
    surcharge_ids: list[str] | None = strawberry.UNSET

    metadata: utils.JSON | None = strawberry.UNSET
    pricing_config: utils.JSON | None = strawberry.UNSET


@strawberry.input
class CreateRateSheetMutationInput(utils.BaseInput):
    name: str
    carrier_name: utils.CarrierNameEnum
    services: list[CreateServiceLevelInput] | None = strawberry.UNSET
    zones: list["SharedZoneInput"] | None = strawberry.UNSET
    surcharges: list["SharedSurchargeInput"] | None = strawberry.UNSET
    service_rates: list["ServiceRateInput"] | None = strawberry.UNSET
    carriers: list[str] | None = strawberry.UNSET
    origin_countries: list[str] | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    pricing_config: utils.JSON | None = strawberry.UNSET


@strawberry.input
class UpdateRateSheetMutationInput(utils.BaseInput):
    id: str
    name: str | None = strawberry.UNSET
    services: list[UpdateServiceLevelInput] | None = strawberry.UNSET
    zones: list["SharedZoneInput"] | None = strawberry.UNSET
    surcharges: list["SharedSurchargeInput"] | None = strawberry.UNSET
    service_rates: list["ServiceRateInput"] | None = strawberry.UNSET
    carriers: list[str] | None = strawberry.UNSET
    origin_countries: list[str] | None = strawberry.UNSET
    remove_missing_services: bool | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    pricing_config: utils.JSON | None = strawberry.UNSET


@strawberry.input
class DeleteRateSheetServiceMutationInput(utils.BaseInput):
    rate_sheet_id: str
    service_id: str


@strawberry.input
class RateSheetFilter(utils.Paginated):
    keyword: str | None = strawberry.UNSET


@strawberry.input
class CreateCarrierConnectionMutationInput(utils.BaseInput):
    carrier_name: utils.CarrierNameEnum
    carrier_id: str
    credentials: utils.JSON
    active: bool | None = True
    config: utils.JSON | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    capabilities: list[str] | None = strawberry.UNSET


@strawberry.input
class UpdateCarrierConnectionMutationInput(utils.BaseInput):
    id: str
    active: bool | None = True
    carrier_id: str | None = strawberry.UNSET
    credentials: utils.JSON | None = strawberry.UNSET
    config: utils.JSON | None = strawberry.UNSET
    metadata: utils.JSON | None = strawberry.UNSET
    capabilities: list[str] | None = strawberry.UNSET


@strawberry.input
class SystemCarrierMutationInput(utils.BaseInput):
    id: str
    enable: bool | None = strawberry.UNSET
    config: utils.JSON | None = strawberry.UNSET
    tc_accepted: bool | None = strawberry.UNSET


@strawberry.input
class CreateMetafieldInput(utils.BaseInput):
    key: str
    type: utils.MetafieldTypeEnum
    value: utils.JSON | None = strawberry.UNSET
    is_required: bool | None = strawberry.UNSET
    object_type: str | None = strawberry.UNSET
    object_id: str | None = strawberry.UNSET


@strawberry.input
class UpdateMetafieldInput(CreateMetafieldInput):
    id: str
    key: str | None = strawberry.UNSET
    type: utils.MetafieldTypeEnum | None = strawberry.UNSET


@strawberry.input
class MetafieldInput(utils.BaseInput):
    key: str
    type: utils.MetafieldTypeEnum
    value: utils.JSON | None = strawberry.UNSET
    is_required: bool | None = strawberry.UNSET
    id: str | None = strawberry.UNSET
    object_type: str | None = strawberry.UNSET
    object_id: str | None = strawberry.UNSET


@strawberry.input
class MetafieldFilter(utils.Paginated):
    key: str | None = strawberry.UNSET
    type: utils.MetafieldTypeEnum | None = strawberry.UNSET
    is_required: bool | None = strawberry.UNSET
    object_type: str | None = strawberry.UNSET
    object_id: str | None = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# SHARED ZONE INPUTS (Rate Sheet Level)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class SharedZoneInput(utils.BaseInput):
    """Input for creating/updating a shared zone at the RateSheet level."""

    label: str
    id: str | None = strawberry.UNSET
    country_codes: list[str] | None = strawberry.UNSET
    postal_codes: list[str] | None = strawberry.UNSET
    cities: list[str] | None = strawberry.UNSET
    transit_days: int | None = strawberry.UNSET
    transit_time: float | None = strawberry.UNSET
    radius: float | None = strawberry.UNSET
    latitude: float | None = strawberry.UNSET
    longitude: float | None = strawberry.UNSET
    # Weight constraints for this zone
    min_weight: float | None = strawberry.UNSET
    max_weight: float | None = strawberry.UNSET
    weight_unit: utils.WeightUnitEnum | None = strawberry.UNSET


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
    id: str | None = strawberry.UNSET
    surcharge_type: str | None = "fixed"  # "fixed" or "percentage"
    cost: float | None = strawberry.UNSET  # COGS
    active: bool | None = True


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
    surcharges: list[SharedSurchargeInput]


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE RATE INPUTS (Service-Zone Rate Mapping)
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class ServiceRateInput(utils.BaseInput):
    """Input for a service-zone rate mapping."""

    service_id: str
    zone_id: str
    rate: float
    cost: float | None = strawberry.UNSET  # COGS
    min_weight: float | None = strawberry.UNSET
    max_weight: float | None = strawberry.UNSET
    transit_days: int | None = strawberry.UNSET
    transit_time: float | None = strawberry.UNSET
    meta: utils.JSON | None = strawberry.UNSET


@strawberry.input
class UpdateServiceRateMutationInput(utils.BaseInput):
    """Update a single service-zone rate."""

    rate_sheet_id: str
    service_id: str
    zone_id: str
    rate: float
    cost: float | None = strawberry.UNSET
    min_weight: float | None = strawberry.UNSET
    max_weight: float | None = strawberry.UNSET
    transit_days: int | None = strawberry.UNSET
    transit_time: float | None = strawberry.UNSET
    meta: utils.JSON | None = strawberry.UNSET


@strawberry.input
class BatchUpdateServiceRatesMutationInput(utils.BaseInput):
    """Batch update multiple service-zone rates."""

    rate_sheet_id: str
    rates: list[ServiceRateInput]


# ─────────────────────────────────────────────────────────────────────────────
# WEIGHT RANGE INPUTS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class AddWeightRangeMutationInput(utils.BaseInput):
    """Add a weight range to a rate sheet (creates rate entries for all service+zone combos)."""

    rate_sheet_id: str
    min_weight: float
    max_weight: float


@strawberry.input
class RemoveWeightRangeMutationInput(utils.BaseInput):
    """Remove a weight range and all its associated rate entries."""

    rate_sheet_id: str
    min_weight: float
    max_weight: float


@strawberry.input
class DeleteServiceRateMutationInput(utils.BaseInput):
    """Delete a specific service rate entry."""

    rate_sheet_id: str
    service_id: str
    zone_id: str
    min_weight: float | None = strawberry.UNSET
    max_weight: float | None = strawberry.UNSET


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE ZONE/SURCHARGE ASSIGNMENT INPUTS
# ─────────────────────────────────────────────────────────────────────────────


@strawberry.input
class UpdateServiceZoneIdsMutationInput(utils.BaseInput):
    """Update zone_ids for a service level."""

    rate_sheet_id: str
    service_id: str
    zone_ids: list[str]


@strawberry.input
class UpdateServiceSurchargeIdsMutationInput(utils.BaseInput):
    """Update surcharge_ids for a service level."""

    rate_sheet_id: str
    service_id: str
    surcharge_ids: list[str]
