"""Karrio Unified model definitions module."""

from unicodedata import category
import attr
from typing import List, Dict, Any, Union
from jstruct import JList, JStruct, REQUIRED


@attr.s(auto_attribs=True)
class Address:
    """shipping party (contact and address) data type."""

    id: str = None
    postal_code: str = None
    city: str = None
    person_name: str = None
    company_name: str = None
    country_code: str = None
    email: str = None
    phone_number: str = None

    state_code: str = None
    residential: bool = False

    address_line1: str = ""
    address_line2: str = None
    street_number: str = None
    suite: str = None

    federal_tax_id: str = None
    state_tax_id: str = None


@attr.s(auto_attribs=True)
class Commodity:
    """commodity or product unified data type."""

    id: str = None
    sku: str = None
    title: str = None
    quantity: int = 1
    hs_code: str = None
    weight: float = None
    weight_unit: str = None
    description: str = None
    value_amount: float = None
    value_currency: str = None
    origin_country: str = None
    category: str = None

    product_url: str = None
    image_url: str = None
    product_id: str = None
    variant_id: str = None
    metadata: Dict = {}


@attr.s(auto_attribs=True)
class Parcel:
    """parcel unified data type."""

    id: str = None
    weight: float = None
    width: float = None
    height: float = None
    length: float = None
    weight_unit: str = None
    dimension_unit: str = None

    packaging_type: str = None
    package_preset: str = None

    is_document: bool = False
    description: str = None
    content: str = None

    items: List[Commodity] = JList[Commodity]
    reference_number: str = None
    freight_class: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class Payment:
    """payment details unified data type."""

    paid_by: str = "sender"
    currency: str = None
    account_number: str = None
    id: str = None


@attr.s(auto_attribs=True)
class Duty:
    """duty payment details unified data type."""

    paid_by: str = "sender"
    currency: str = None
    account_number: str = None
    declared_value: float = None
    id: str = None


@attr.s(auto_attribs=True)
class Customs:
    """customs info unified data type."""

    commodities: List[Commodity] = JList[Commodity, REQUIRED]
    certify: bool = None
    signer: str = None
    content_type: str = None
    content_description: str = None
    incoterm: str = None
    invoice: str = None
    invoice_date: str = None
    duty: Duty = JStruct[Duty]
    duty_billing_address: Address = JStruct[Address]
    commercial_invoice: bool = False
    options: Dict = {}
    id: str = None


@attr.s(auto_attribs=True)
class ShipmentRequest:
    """shipment request unified data type."""

    service: str

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    return_address: Address = JStruct[Address]
    billing_address: Address = JStruct[Address]

    options: Dict = {}
    reference: str = ""
    label_type: str = None

    metadata: Dict = {}


@attr.s(auto_attribs=True)
class ShipmentCancelRequest:
    """shipment cancellation request unified data type."""

    shipment_identifier: str

    service: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class RateRequest:
    """rate fetching request unified data type."""

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    return_address: Address = JStruct[Address]
    billing_address: Address = JStruct[Address]

    services: List[str] = []
    options: Dict = {}
    reference: str = ""


@attr.s(auto_attribs=True)
class TrackingRequest:
    """tracking request unified data type."""

    tracking_numbers: List[str]
    account_numer: str = None
    reference: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupRequest:
    """pickup request unified data type."""

    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    parcels_count: int = None
    shipment_identifiers: List[str] = []
    package_location: str = None
    instruction: str = None
    pickup_type: str = "one_time"  # one_time, daily, recurring
    recurrence: Dict = {}  # For recurring: {frequency, days_of_week, end_date}
    options: Dict = {}
    metadata: Dict = {}


@attr.s(auto_attribs=True)
class PickupUpdateRequest:
    """pickup update request unified data type."""

    confirmation_number: str
    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    shipment_identifiers: List[str] = []
    package_location: str = None
    instruction: str = None
    pickup_type: str = "one_time"  # one_time, daily, recurring
    recurrence: Dict = {}  # For recurring: {frequency, days_of_week, end_date}
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupCancelRequest:
    """pickup cancellation request unified data type."""

    confirmation_number: str

    address: Address = JStruct[Address]
    pickup_date: str = None
    reason: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class AddressValidationRequest:
    """address validation request unified data type."""

    address: Address = JStruct[Address, REQUIRED]
    options: Dict = {}


@attr.s(auto_attribs=True)
class ManifestRequest:
    """manifest request unified data type."""

    shipment_identifiers: List[str]
    address: Address = JStruct[Address, REQUIRED]

    reference: str = None
    metadata: Dict = {}
    options: Dict = {}


@attr.s(auto_attribs=True)
class ChargeDetails:
    """Karrio unified charge data type."""

    name: str = None
    amount: float = None  # Sell price (shown to customer)
    currency: str = None
    id: str = None

    # Enhanced fields for accounting and transparency
    cost: float = None  # COGS - Cost of Goods Sold (internal)
    charge_type: str = None  # "base" | "surcharge" | "addon" | "tax"
    metadata: Dict = None  # Extra metadata (only set when needed)


@attr.s(auto_attribs=True)
class DutiesCalculationRequest:
    """duties calculation request unified data type."""

    shipment_identifier: str
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    customs: Customs = JStruct[Customs, REQUIRED]

    shipping_charge: ChargeDetails = JStruct[ChargeDetails]
    insurance_charge: ChargeDetails = JStruct[ChargeDetails]
    reference: str = None
    metadata: Dict = {}
    options: Dict = {}


@attr.s(auto_attribs=True)
class InsuranceRequest:
    """insurance request unified data type."""

    shipment_identifier: str
    amount: float
    currency: str
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcel: Parcel = JStruct[Parcel, REQUIRED]

    provider: str = None
    reference: str = None
    metadata: Dict = {}
    options: Dict = {}


@attr.s(auto_attribs=True)
class WebhookRegistrationRequest:
    """webhook registration request unified data type."""

    url: str
    description: str = None
    enabled_events: List[str] = []
    options: Dict = {}
    metadata: Dict = {}


@attr.s(auto_attribs=True)
class WebhookDeregistrationRequest:
    """webhook deregistration request unified data type."""

    webhook_id: str
    options: Dict = {}


@attr.s(auto_attribs=True)
class Message:
    """Karrio unified Message data type."""

    carrier_name: str
    carrier_id: str

    message: Union[str, Any] = None
    level: str = None
    code: str = None
    details: Dict = None


@attr.s(auto_attribs=True)
class AddressValidationDetails:
    """Karrio unified address validation details data type."""

    carrier_name: str
    carrier_id: str
    success: bool
    complete_address: Address = None


@attr.s(auto_attribs=True)
class TrackingEvent:
    """Karrio unified tracking event data type."""

    date: str
    description: str
    code: str = None
    time: str = None
    timestamp: str = None  # ISO 8601 format "2025-12-04T07:16:00.000Z"
    status: str = None  # Normalized status (TrackerStatus enum value name)
    reason: str = None  # Normalized reason (TrackingIncidentReason enum value name)
    location: str = None

    # Geolocation
    latitude: float = None
    longitude: float = None


@attr.s(auto_attribs=True)
class RateDetails:
    """Karrio unified rate (quote) details data type."""

    carrier_name: str
    carrier_id: str
    service: str
    currency: str = None
    total_charge: float = 0.0
    extra_charges: List[ChargeDetails] = JList[ChargeDetails]
    estimated_delivery: str = None
    transit_days: int = None
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class TrackingInfo:
    """Karrio unified tracking details data type."""

    carrier_tracking_link: str = None
    customer_name: str = None
    expected_delivery: str = None
    note: str = None
    order_date: str = None
    order_id: str = None
    package_weight: str = None
    package_weight_unit: str = None
    shipment_package_count: str = None
    shipment_pickup_date: str = None
    shipment_delivery_date: str = None
    shipment_service: str = None
    shipment_origin_country: str = None
    shipment_origin_postal_code: str = None
    shipment_destination_country: str = None
    shipment_destination_postal_code: str = None
    shipping_date: str = None
    signed_by: str = None
    source: str = None


@attr.s(auto_attribs=True)
class Images:
    """Karrio unified tracker images data type."""

    delivery_image: str = None
    signature_image: str = None


@attr.s(auto_attribs=True)
class TrackingDetails:
    """Karrio unified tracking details data type."""

    carrier_name: str
    carrier_id: str
    tracking_number: str
    events: List[TrackingEvent] = JList[TrackingEvent, REQUIRED]
    images: Images = JStruct[Images]
    estimated_delivery: str = None
    info: TrackingInfo = None
    delivered: bool = None
    status: str = None
    meta: dict = None


@attr.s(auto_attribs=True)
class ShippingDocument:
    """Karrio unified shipping document data type."""

    category: str
    format: str = "PDF"
    print_format: str = None
    base64: str = None
    url: str = None


@attr.s(auto_attribs=True)
class Documents:
    """Karrio unified shipment documents details data type."""

    label: str = None

    invoice: str = None
    zpl_label: str = None
    pdf_label: str = None
    extra_documents: List[ShippingDocument] = JList[ShippingDocument]


@attr.s(auto_attribs=True)
class ShipmentDetails:
    """Karrio unified shipment details data type."""

    carrier_name: str
    carrier_id: str
    tracking_number: str
    shipment_identifier: str
    docs: Documents = JStruct[Documents, REQUIRED]
    selected_rate: RateDetails = JStruct[RateDetails]
    label_type: str = None
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class PickupDetails:
    """Karrio unified pickup details data type."""

    carrier_name: str
    carrier_id: str
    confirmation_number: str
    pickup_date: str = None
    pickup_charge: ChargeDetails = JStruct[ChargeDetails]
    ready_time: str = None
    closing_time: str = None
    pickup_type: str = None  # one_time, daily, recurring
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class ManifestDocument:
    """Karrio unified manifest document details data type."""

    manifest: str = None


@attr.s(auto_attribs=True)
class ManifestDetails:
    """Karrio unified manifest details data type."""

    carrier_name: str
    carrier_id: str
    doc: ManifestDocument = JStruct[ManifestDocument]
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class ConfirmationDetails:
    """Karrio unified binary operation confirmation data type."""

    carrier_name: str
    carrier_id: str
    success: bool
    operation: str


@attr.s(auto_attribs=True)
class DutiesCalculationDetails:
    """Karrio unified duties calculation details data type."""

    carrier_name: str
    carrier_id: str
    total_charge: float
    currency: str

    charges: List[ChargeDetails] = JList[ChargeDetails]
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class InsuranceDetails:
    """Karrio unified insurance details data type."""

    carrier_name: str
    carrier_id: str

    fees: List[ChargeDetails] = JList[ChargeDetails]
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class WebhookRegistrationDetails:
    """Karrio unified webhook registration details data type."""

    carrier_name: str
    carrier_id: str
    secret: str

    webhook_identifier: str = None
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class WebhookEventDetails:
    """Karrio unified webhook event data details data type."""

    carrier_name: str
    carrier_id: str

    tracking_number: str = None
    shipment_identifier: str = None
    tracking: TrackingDetails = JStruct[TrackingDetails]
    shipment: ShipmentDetails = JStruct[ShipmentDetails]


@attr.s(auto_attribs=True)
class OAuthAuthorizePayload:
    """Karrio unified OAuth authorize request data type."""

    redirect_uri: str
    state: str
    options: Dict = {}


@attr.s(auto_attribs=True)
class OAuthAuthorizeRequest:
    """Karrio unified OAuth authorize response data type."""

    carrier_name: str
    authorization_url: str

    state: str = None
    meta: Dict = {}


@attr.s(auto_attribs=True)
class RequestPayload:
    """Karrio unified hooks request payload data type."""

    url: str
    body: dict = {}
    query: dict = {}
    headers: dict = {}


# ─────────────────────────────────────────────────────────────────────────────
# SHARED ZONE (Rate Sheet Level - for optimized structure)
# ─────────────────────────────────────────────────────────────────────────────


@attr.s(auto_attribs=True)
class ServiceZone:
    """Karrio unified service zone.

    Represents a geographic zone with specific rate and delivery parameters.
    Used by the rating proxy for rate calculations.
    """

    id: str = None
    label: str = None
    rate: float = None  # Sell price for this zone
    cost: float = None  # COGS - Cost of Goods Sold for this zone

    # Weight restrictions
    min_weight: float = None
    max_weight: float = None

    # Estimated delivery
    transit_days: int = None
    transit_time: float = None

    # Geolocation
    radius: float = None
    latitude: float = None
    longitude: float = None

    # Location matching
    cities: List[str] = []
    postal_codes: List[str] = []
    country_codes: List[str] = []


@attr.s(auto_attribs=True)
class Surcharge:
    """Karrio unified surcharge data type.

    Represents a surcharge that can be applied to shipping rates.
    Used by the rating proxy for rate calculations.
    """

    id: str = None
    name: str = None
    amount: float = None  # Sell price (shown to customer)
    surcharge_type: str = "fixed"  # "fixed" or "percentage"
    cost: float = None  # COGS - Cost of Goods Sold
    active: bool = True


@attr.s(auto_attribs=True)
class SharedZone:
    """Shared zone definition at the RateSheet level.

    Zones are defined once at the rate sheet level and referenced by ID
    from ServiceLevel.zone_ids. This eliminates duplication when multiple
    services share the same geographic zones.
    """

    id: str
    label: str = None

    # Location matching
    country_codes: List[str] = []
    postal_codes: List[str] = []
    cities: List[str] = []

    # Default transit times (can be overridden in service_rates)
    transit_days: int = None
    transit_time: float = None

    # Geolocation (for radius-based matching)
    radius: float = None
    latitude: float = None
    longitude: float = None

    metadata: Dict = {}


# ─────────────────────────────────────────────────────────────────────────────
# SHARED SURCHARGE (Rate Sheet Level - for optimized structure)
# ─────────────────────────────────────────────────────────────────────────────


@attr.s(auto_attribs=True)
class SharedSurcharge:
    """Shared surcharge definition at the RateSheet level.

    Surcharges are defined once at the rate sheet level and referenced by ID
    from ServiceLevel.surcharge_ids. This allows updating a surcharge
    (e.g., fuel percentage) in one place to affect all services.
    """

    id: str
    name: str
    amount: float = 0  # Sell price (shown to customer)
    surcharge_type: str = "fixed"  # "fixed" or "percentage"
    cost: float = None  # COGS - Cost of Goods Sold
    active: bool = True
    metadata: Dict = {}


# ─────────────────────────────────────────────────────────────────────────────
# SERVICE RATE (Service-Zone Rate Mapping)
# ─────────────────────────────────────────────────────────────────────────────


@attr.s(auto_attribs=True)
class ServiceRate:
    """Rate for a specific service-zone combination.

    Stored in RateSheet.service_rates to map services to zones with
    specific rates and weight constraints.
    """

    service_id: str
    zone_id: str
    rate: float = 0  # Sell price
    cost: float = None  # COGS

    # Weight constraints (override zone defaults)
    min_weight: float = None
    max_weight: float = None

    # Transit time overrides
    transit_days: int = None
    transit_time: float = None


# SERVICE LEVEL FEATURES (Structured feature definitions)
# ─────────────────────────────────────────────────────────────────────────────


@attr.s(auto_attribs=True)
class ServiceLevelFeatures:
    """Structured feature definitions for a shipping service.

    All fields are optional with sensible defaults. These features are used for:
    - Filtering available services based on requirements
    - Setting default options during shipping method configuration
    - Displaying service capabilities in the UI
    """

    # First Mile: How parcels get to the carrier
    # "pick_up" = carrier picks up from sender
    # "drop_off" = sender drops off at carrier location
    # "pick_up_and_drop_off" = both options available
    first_mile: str = None

    # Last Mile: How parcels are delivered to recipient
    # "home_delivery" = delivered to recipient's address
    # "service_point" = delivered to pickup point/locker
    # "mailbox" = delivered to mailbox (small items)
    last_mile: str = None

    # Form Factor: Type of package the service supports
    # "letter" = flat mail/documents
    # "parcel" = standard packages
    # "mailbox" = fits in standard mailbox
    # "pallet" = freight/palletized goods
    form_factor: str = None

    # Type of Shipments: Business model support
    # True/False for each, both can be True
    b2c: bool = None  # Business to Consumer
    b2b: bool = None  # Business to Business

    # Shipment Direction
    # "outbound" = from sender to recipient
    # "returns" = return shipments
    # "both" = supports both directions
    shipment_type: str = None

    # Age Verification
    # None = no age check
    # "16" = 16+ verification
    # "18" = 18+ verification
    age_check: str = None

    # Signature Required by default
    signature: bool = None

    # Tracking
    tracked: bool = None

    # Insurance available
    insurance: bool = None

    # Express/Priority service
    express: bool = None

    # Dangerous goods support
    dangerous_goods: bool = None

    # Weekend delivery options
    saturday_delivery: bool = None
    sunday_delivery: bool = None

    # Multi-package shipment support
    multicollo: bool = None

    # Neighbor delivery allowed
    neighbor_delivery: bool = None


# ─────────────────────────────────────────────────────────────────────────────


@attr.s(auto_attribs=True)
class ServiceLevel:
    """Karrio unified service level data type.

    Represents a shipping service with rate definitions and restrictions.
    For rate calculation, zones and surcharges are populated at runtime
    from the rate sheet data.
    """

    service_name: str
    service_code: str
    carrier_service_code: str = None
    description: str = ""
    active: bool = True
    id: str = None

    # Rate definitions
    currency: str = None

    # Zone data for rate calculation (populated at runtime from rate sheet)
    zones: List[ServiceZone] = JList[ServiceZone]

    # Surcharge data for rate calculation (populated at runtime from rate sheet)
    surcharges: List[Surcharge] = JList[Surcharge]

    # References to shared zones/surcharges at RateSheet level (for storage)
    zone_ids: List[str] = []
    surcharge_ids: List[str] = []

    # Cost tracking (internal - not shown to customer)
    cost: float = None  # Base COGS - Cost of Goods Sold

    # Weight restrictions
    min_weight: float = None
    max_weight: float = None
    weight_unit: str = None

    # Size restrictions
    max_width: float = None
    max_height: float = None
    max_length: float = None
    dimension_unit: str = None

    # Volumetric weight
    max_volume: float = None  # Maximum volume in liters

    # Dimensional/Volumetric weight calculation
    dim_factor: float = None  # Divisor: 5000-6000 for cm/kg, 139-166 for in/lb
    use_volumetric: bool = False  # Use max(actual, volumetric) for rate calc

    # Origin restrictions (optional - inherits from rate sheet if not set)
    origin_countries: List[str] = []

    # Destination supports
    domicile: bool = None
    international: bool = None

    # Estimated delivery
    transit_days: int = None
    transit_time: float = None

    # Service features as structured object
    # Contains first_mile, last_mile, form_factor, b2c, b2b, shipment_type, etc.
    features: ServiceLevelFeatures = JStruct[ServiceLevelFeatures]

    metadata: Dict = {}


# ─────────────────────────────────────────────────────────────────────────────
# RATE SHEET (Complete rate configuration)
# ─────────────────────────────────────────────────────────────────────────────


@attr.s(auto_attribs=True)
class RateSheet:
    """Karrio unified rate sheet data type.

    A complete rate configuration with shared zones, surcharges, and services.
    Uses the optimized structure where zones and surcharges are defined once
    and referenced by ID.
    """

    id: str
    name: str
    carrier_name: str
    slug: str = None

    # Shared definitions (referenced by ID from services)
    zones: List[SharedZone] = JList[SharedZone]
    surcharges: List[SharedSurcharge] = JList[SharedSurcharge]

    # Service-zone rate mappings
    service_rates: List[ServiceRate] = JList[ServiceRate]

    # Service definitions
    services: List[ServiceLevel] = JList[ServiceLevel]

    metadata: Dict = {}


@attr.s(auto_attribs=True)
class LabelTemplate:
    """Karrio unified label template data type."""

    slug: str
    template: str
    template_type: str = "SVG"  # ZPL, SVG
    width: int = 4
    height: int = 6

    id: str = None


@attr.s(auto_attribs=True)
class ServiceLabel:
    """Karrio unified service label data type."""

    label: str
    label_type: str
    service_name: str
    service_code: str
    tracking_number: str


@attr.s(auto_attribs=True)
class DocumentFile:
    """shipment document unified data type."""

    doc_file: str  #  base64 encoded string
    doc_name: str
    doc_type: str = None
    doc_format: str = None


@attr.s(auto_attribs=True)
class DocumentUploadRequest:
    """shipment document upload request unified data type."""

    document_files: List[DocumentFile] = JList[DocumentFile, REQUIRED]
    tracking_number: str = None
    shipment_date: str = None
    reference: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class DocumentDetails:
    """Karrio unified uploaded document id info data type."""

    doc_id: str
    file_name: str


@attr.s(auto_attribs=True)
class DocumentUploadDetails:
    """Karrio unified shipment document upload details data type."""

    carrier_name: str
    carrier_id: str
    documents: List[DocumentDetails] = JList[DocumentDetails]
    meta: dict = None
    id: str = None
