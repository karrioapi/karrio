"""Karrio Unified model definitions module."""
import attr
from typing import List, Dict, Any, Union
from jstruct import JList, JStruct, REQUIRED


@attr.s(auto_attribs=True)
class AddressExtra:
    street_name: str = None
    street_number: str = None
    street_type: str = None
    suburb: str = None
    suite: str = None


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
    address_line2: str = ""

    federal_tax_id: str = None
    state_tax_id: str = None

    extra: AddressExtra = JStruct[AddressExtra]


@attr.s(auto_attribs=True)
class Commodity:
    """commodity or product unified data type."""

    id: str = None
    sku: str = None
    hs_code: str = None
    quantity: int = 1
    weight: float = None
    weight_unit: str = None
    description: str = None
    value_amount: float = None
    value_currency: str = None
    origin_country: str = None

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
    address: Address = JStruct[Address]
    id: str = None


@attr.s(auto_attribs=True)
class Duty:
    """duty payment details unified data type."""

    paid_by: str = "sender"
    currency: str = None
    account_number: str = None
    declared_value: float = None
    bill_to: Address = JStruct[Address]
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

    services: List[str] = []
    options: Dict = {}
    reference: str = ""


@attr.s(auto_attribs=True)
class TrackingRequest:
    """tracking request unified data type."""

    tracking_numbers: List[str]
    language_code: str = None
    level_of_details: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupRequest:
    """pickup request unified data type."""

    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    instruction: str = None
    package_location: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupUpdateRequest:
    """pickup update request unified data type."""

    confirmation_number: str
    pickup_date: str
    ready_time: str
    closing_time: str
    address: Address = JStruct[Address, REQUIRED]

    parcels: List[Parcel] = JList[Parcel]
    instruction: str = None
    package_location: str = None
    options: Dict = {}


@attr.s(auto_attribs=True)
class PickupCancelRequest:
    """pickup cancellation request unified data type."""

    confirmation_number: str

    address: Address = JStruct[Address]
    pickup_date: str = None
    reason: str = None


@attr.s(auto_attribs=True)
class AddressValidationRequest:
    """address validation request unified data type."""

    address: Address = JStruct[Address, REQUIRED]


@attr.s(auto_attribs=True)
class Message:
    """Karrio unified Message data type."""

    carrier_name: str
    carrier_id: str
    message: Union[str, Any] = None
    code: str = None
    details: Dict = None


@attr.s(auto_attribs=True)
class ChargeDetails:
    """Karrio unified charge data type."""

    name: str = None
    amount: float = None
    currency: str = None


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
    location: str = None
    code: str = None
    time: str = None


@attr.s(auto_attribs=True)
class RateDetails:
    """Karrio unified rate (quote) details data type."""

    carrier_name: str
    carrier_id: str
    service: str
    currency: str = None
    total_charge: float = 0.0
    transit_days: int = None
    extra_charges: List[ChargeDetails] = JList[ChargeDetails]
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class TrackingDetails:
    """Karrio unified tracking details data type."""

    carrier_name: str
    carrier_id: str
    tracking_number: str
    events: List[TrackingEvent] = JList[TrackingEvent, REQUIRED]
    delivered: bool = None
    estimated_delivery: str = None
    meta: dict = None


@attr.s(auto_attribs=True)
class Documents:
    """Karrio unified shipment details data type."""

    label: str
    invoice: str = None


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
    id: str = None


@attr.s(auto_attribs=True)
class ConfirmationDetails:
    """Karrio unified binary operation confirmation data type."""

    carrier_name: str
    carrier_id: str
    success: bool
    operation: str


@attr.s(auto_attribs=True)
class ServiceLevel:
    """Karrio unified service level data type."""

    service_name: str
    service_code: str
    description: str = ""
    id: str = None
    active: bool = True

    # Costs definition
    cost: float = None
    currency: str = None

    # Estimated delivery date
    estimated_transit_days: int = None

    # Size restrictions
    max_weight: float = None
    max_width: float = None
    max_height: float = None
    max_length: float = None
    weight_unit: str = None
    dimension_unit: str = None

    # Destination supports
    domicile: bool = None
    international: bool = None


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
    options: Dict = {}
    reference: str = None
    tracking_number: str = None


@attr.s(auto_attribs=True)
class DocumentDetails:
    """Karrio unified uploaded document id info data type."""

    document_id: str
    file_name: str


@attr.s(auto_attribs=True)
class DocumentUploadDetails:
    """Karrio unified shipment document upload details data type."""

    carrier_name: str
    carrier_id: str
    documents: List[DocumentDetails] = JList[DocumentDetails]
    meta: dict = None
    id: str = None
