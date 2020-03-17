"""PurplShip Unified datatypes module."""
import attr
from typing import List, Dict
from jstruct import JList, JStruct, REQUIRED


@attr.s(auto_attribs=True)
class Address:
    """shipping party (contact and address) type."""

    postal_code: str = None
    city: str = None
    type: str = None
    federal_tax_id: str = None
    state_tax_id: str = None
    person_name: str = None
    company_name: str = None
    country_code: str = None
    email_address: str = None
    phone_number: str = None

    state_code: str = None
    suburb: str = None
    residential: bool = False

    address_line_1: str = ""
    address_line_2: str = ""


@attr.s(auto_attribs=True)
class Commodity:
    """item type is a commodity."""

    id: str = None
    weight: float = None
    width: float = None
    height: float = None
    length: float = None
    description: str = None
    quantity: int = 1
    sku: str = None
    value_amount: float = None
    value_currency: str = None
    origin_country: str = None


@attr.s(auto_attribs=True)
class Parcel:
    """item type."""

    weight: float
    id: str = None
    width: float = None
    height: float = None
    length: float = None
    packaging_type: str = None
    reference: str = ""
    description: str = None
    content: str = None
    is_document: bool = False
    weight_unit: str = "LB"
    dimension_unit: str = "IN"
    services: List[str] = []
    options: Dict = {}


@attr.s(auto_attribs=True)
class Invoice:
    """invoice type."""

    date: str
    identifier: str = None
    type: str = None
    copies: int = None


@attr.s(auto_attribs=True)
class Payment:
    """payment configuration type."""

    paid_by: str = None
    description: str = None
    amount: float = None
    currency: str = None
    account_number: str = None


@attr.s(auto_attribs=True)
class Customs:
    """customs type."""

    no_eei: str = None
    aes: str = None
    description: str = None
    terms_of_trade: str = None
    commodities: List[Commodity] = JList[Commodity]
    duty: Payment = JStruct[Payment]
    invoice: Invoice = JStruct[Invoice]
    commercial_invoice: bool = False


@attr.s(auto_attribs=True)
class Doc:
    """document image type."""

    type: str = None
    format: str = None
    image: str = None


@attr.s(auto_attribs=True)
class ShipmentRequest:
    """shipment request type."""

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcel: Parcel = JStruct[Parcel, REQUIRED]

    label: Doc = JStruct[Doc]
    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    doc_images: List[Doc] = JList[Doc]

    options: Dict = {}


@attr.s(auto_attribs=True)
class RateRequest:
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcel: Parcel = JStruct[Parcel, REQUIRED]


@attr.s(auto_attribs=True)
class TrackingRequest:
    """tracking request type."""

    tracking_numbers: List[str]
    language_code: str = None
    level_of_details: str = None


@attr.s(auto_attribs=True)
class PickupRequest:
    """pickup request type."""

    date: str

    address: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    ready_time: str = None
    closing_time: str = None
    instruction: str = None
    package_location: str = None


@attr.s(auto_attribs=True)
class PickupUpdateRequest:
    """pickup update request type."""

    date: str
    address: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    confirmation_number: str = None
    ready_time: str = None
    closing_time: str = None
    instruction: str = None
    package_location: str = None


@attr.s(auto_attribs=True)
class PickupCancellationRequest:
    """pickup cancellation request type."""

    pickup_date: str
    confirmation_number: str
    person_name: str = None
    country_code: str = None


""" Unified option data types """


@attr.s(auto_attribs=True)
class COD:
    """cash on delivery option type."""

    amount: float
    currency: str


@attr.s(auto_attribs=True)
class Insurance:
    """insurance option type."""

    amount: float
    currency: str
    provider: str
    description: str = None


""" Unified response data types """


@attr.s(auto_attribs=True)
class Error:
    """PurplShip Error type."""

    message: str = None
    code: str = None
    carrier: str = None
    details: dict = None


@attr.s(auto_attribs=True)
class ChargeDetails:
    """PurplShip charge type."""

    name: str = None
    amount: float = None
    currency: str = None


@attr.s(auto_attribs=True)
class ReferenceDetails:
    """PurplShip reference details type."""

    value: str
    type: str = None


@attr.s(auto_attribs=True)
class TimeDetails:
    """PurplShip time details type."""

    value: str
    name: str = None


@attr.s(auto_attribs=True)
class TrackingEvent:
    """PurplShip tracking event type."""

    date: str
    description: str
    location: str
    code: str
    time: str = None
    signatory: str = None


@attr.s(auto_attribs=True)
class RateDetails:
    """PurplShip rate (quote) details type."""

    carrier: str
    service_name: str
    currency: str
    service_type: str = None
    discount: float = 0.0
    base_charge: float = 0.0
    delivery_date: str = None
    total_charge: float = 0.0
    duties_and_taxes: float = 0.0
    extra_charges: List[ChargeDetails] = []


@attr.s(auto_attribs=True)
class TrackingDetails:
    """PurplShip tracking details type."""

    carrier: str
    tracking_number: str
    shipment_date: str = None
    events: List[TrackingEvent] = []


@attr.s(auto_attribs=True)
class ShipmentDetails:
    """PurplShip shipment details type."""

    carrier: str
    tracking_number: List[str]
    total_charge: ChargeDetails
    charges: List[ChargeDetails]
    shipment_date: str = None
    service: str = None
    documents: List[str] = []
    reference: ReferenceDetails = None


@attr.s(auto_attribs=True)
class PickupDetails:
    """PurplShip pickup details type."""

    carrier: str
    confirmation_number: str
    pickup_date: str = None
    pickup_charge: ChargeDetails = None
    ref_times: List[TimeDetails] = None
