"""PurplShip Unified datatypes module."""
import attr
from typing import List, Dict
from jstruct import JList, JStruct, REQUIRED


@attr.s(auto_attribs=True)
class Address:
    """shipping party (contact and address) type."""

    id: str = None
    postal_code: str = None
    city: str = None
    federal_tax_id: str = None
    state_tax_id: str = None
    person_name: str = None
    company_name: str = None
    country_code: str = None
    email: str = None
    phone_number: str = None

    state_code: str = None
    suburb: str = None
    residential: bool = False

    address_line1: str = ""
    address_line2: str = ""


@attr.s(auto_attribs=True)
class Commodity:
    """item type is a commodity."""

    id: str = None
    weight: float = None
    description: str = None
    quantity: int = 1
    sku: str = None
    value_amount: float = None
    value_currency: str = None
    origin_country: str = None


@attr.s(auto_attribs=True)
class Parcel:
    """item type."""

    id: str = None
    weight: float = None
    width: float = None
    height: float = None
    length: float = None
    packaging_type: str = None
    package_preset: str = None
    description: str = None
    content: str = None
    is_document: bool = False
    weight_unit: str = None
    dimension_unit: str = None


@attr.s(auto_attribs=True)
class Invoice:
    """invoice type."""

    date: str
    identifier: str = None
    type: str = None
    copies: int = None


@attr.s(auto_attribs=True)
class Card:
    """Credit Card type."""

    type: str
    number: str
    expiry_month: str
    expiry_year: str
    security_code: str
    name: str = None
    postal_code: str = None


@attr.s(auto_attribs=True)
class Payment:
    """payment configuration type."""

    paid_by: str = "sender"
    amount: float = None
    currency: str = None
    account_number: str = None
    credit_card: Card = JStruct[Card]
    contact: Address = JStruct[Address]


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

    service: str

    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    payment: Payment = JStruct[Payment]
    customs: Customs = JStruct[Customs]
    doc_images: List[Doc] = JList[Doc]

    options: Dict = {}
    reference: str = ""


@attr.s(auto_attribs=True)
class RateRequest:
    shipper: Address = JStruct[Address, REQUIRED]
    recipient: Address = JStruct[Address, REQUIRED]
    parcels: List[Parcel] = JList[Parcel, REQUIRED]

    services: List[str] = []
    options: Dict = {}
    reference: str = ""


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


@attr.s(auto_attribs=True)
class Notification:
    """notification option type."""

    email: str = None  # Only defined if other email than shipper
    locale: str = "en"


@attr.s(auto_attribs=True)
class Insurance:
    """insurance option type."""

    amount: float


""" Unified response data types """


@attr.s(auto_attribs=True)
class Message:
    """PurplShip Message type."""

    carrier_name: str
    carrier_id: str
    message: str = None
    code: str = None
    details: Dict = None


@attr.s(auto_attribs=True)
class ChargeDetails:
    """PurplShip charge type."""

    name: str = None
    amount: float = None
    currency: str = None


@attr.s(auto_attribs=True)
class TrackingEvent:
    """PurplShip tracking event type."""

    date: str
    description: str
    location: str
    code: str = None
    time: str = None
    signatory: str = None


@attr.s(auto_attribs=True)
class RateDetails:
    """PurplShip rate (quote) details type."""

    carrier_name: str
    carrier_id: str
    currency: str
    transit_days: int = None
    service: str = None
    discount: float = None
    base_charge: float = 0.0
    total_charge: float = 0.0
    duties_and_taxes: float = None
    extra_charges: List[ChargeDetails] = JList[ChargeDetails]
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class TrackingDetails:
    """PurplShip tracking details type."""

    carrier_name: str
    carrier_id: str
    tracking_number: str
    events: List[TrackingEvent] = JList[TrackingEvent, REQUIRED]


@attr.s(auto_attribs=True)
class ShipmentDetails:
    """PurplShip shipment details type."""

    carrier_name: str
    carrier_id: str
    label: str
    tracking_number: str
    selected_rate: RateDetails = JStruct[RateDetails]
    meta: dict = None
    id: str = None


@attr.s(auto_attribs=True)
class PickupDetails:
    """PurplShip pickup details type."""

    carrier_name: str
    carrier_id: str
    confirmation_number: str
    pickup_date: str = None
    pickup_charge: ChargeDetails = JStruct[ChargeDetails]
    ready_time: str = None
    closing_time: str = None
    id: str = None
