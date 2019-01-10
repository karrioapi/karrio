from typing import List, NamedTuple, Dict, Optional

class party(NamedTuple):
    postal_code: Optional[str] = None
    city: Optional[str] = None
    type: Optional[str] = None
    tax_id: Optional[str] = None
    account_number: Optional[str] = None
    person_name: Optional[str] = None
    company_name: Optional[str] = None
    country_name: Optional[str] = None
    country_code: Optional[str] = None
    email_address: Optional[str] = None
    phone_number: Optional[str] = None

    """ state or province """
    state: Optional[str] = None
    state_code: Optional[str] = None

    address_lines: List[str] = []
    extra: Dict = {}

class item_type(NamedTuple):
    """
        item type is a package or a commodity
    """

    weight: float
    id: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    length: Optional[float] = None
    packaging_type: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    quantity: int = 1
    sku: Optional[str] = None
    code: Optional[str] = None
    value_amount: Optional[float] = None
    value_currency: Optional[str] = None
    origin_country: Optional[str] = None
    extra: Dict = {}

class customs_type(NamedTuple):
    no_eei: Optional[str] = None
    aes: Optional[str] = None
    description: Optional[str] = None
    terms_of_trade: Optional[str] = None
    items: List[item_type] = []
    commercial_invoice: bool = False
    extra: Dict = {}

class invoice_type(NamedTuple):
    date: str
    identifier: Optional[str] = None
    type: Optional[str] = None
    copies: Optional[int] = None
    extra: Dict = {}

class doc_image(NamedTuple):
    type: Optional[str] = None
    format: Optional[str] = None
    image: Optional[str] = None
    extra: Dict = {}

class option_type(NamedTuple):
    code: str 
    value: Dict = {}
    extra: Dict = {}

class shipment_options(NamedTuple):

    """ packages or commodities """
    items: List[item_type]

    insured_amount: Optional[float] = None
    total_items: Optional[int] = None
    packaging_type: Optional[str] = None
    is_document: bool = False
    total_weight: Optional[float] = None
    weight_unit: str = "LB"
    dimension_unit: str = "IN"

    currency: Optional[str] = None
    paid_by: Optional[str] = None
    declared_value: Optional[float] = None
    payment_type: Optional[str] = None
    duty_paid_by: Optional[str] = None
    duty_payment_account: Optional[str] = None
    payment_country_code: Optional[str] = None
    payment_account_number: Optional[str] = None

    date: Optional[str] = None
    customs: Optional[customs_type] = None
    invoice: Optional[invoice_type] = None
    doc_images: List[doc_image] = []
    
    references: List[str] = []
    services: List[str] = []
    options: List[option_type] = []

    label: Optional[doc_image] = None
    extra: Dict = {}

class shipment_request(NamedTuple):
    shipper: party 
    recipient: party
    shipment: shipment_options

class tracking_request(NamedTuple):
    tracking_numbers: List[str]
    language_code: Optional[str] = None
    level_of_details: Optional[str] = None
    extra: Dict = {}

class pickup_request(NamedTuple):
    date: str
    account_number: str
    weight: Optional[float] = None
    weight_unit: Optional[str] = None
    pieces: Optional[float] = None
    ready_time: Optional[str] = None
    closing_time: Optional[str] = None
    instruction: Optional[str] = None
    package_location: Optional[str] = None

    city: Optional[str] = None
    postal_code: Optional[str] = None
    person_name: Optional[str] = None
    company_name: Optional[str] = None
    phone_number: Optional[str] = None
    email_address: Optional[str] = None
    is_business: bool = True

    """ state or province """
    state: Optional[str] = None
    state_code: Optional[str] = None

    country_name: Optional[str] = None
    country_code: Optional[str] = None

    """ required for pickup modification """
    confirmation_number: Optional[str] = None

    address_lines: List[str] = []
    extra: Dict = {}   

class pickup_cancellation_request(NamedTuple):
    pickup_date: str
    confirmation_number: str
    person_name: Optional[str] = None
    country_code: Optional[str] = None
    extra: Dict = {}   

''' Generic response data types '''

class Error():
    def __init__(self, message: str = None, code: str = None, carrier: str = None):
        self.message = message
        self.code = code
        self.carrier = carrier

class ChargeDetails:
    def __init__(self, name: str = None, amount: str = None, currency: str = None):
        self.name = name
        self.amount = amount
        self.currency = currency

class ReferenceDetails:
    def __init__(self, value: str, type: str = None):
        self.value = value
        self.type = type

class TimeDetails:
    def __init__(self, value: str, name: str = None):
        self.value = value
        self.name = name

class TrackingEvent:
    def __init__(self, date: str, description: str, location: str, code: str, time: str = None, signatory: str = None):
        self.date = date
        self.time = time
        self.description = description
        self.location = location
        self.code = code
        self.signatory = signatory

class QuoteDetails:
    def __init__(self, carrier: str, service_name: str, service_type: str, 
        base_charge: float, duties_and_taxes: float, total_charge: float, currency: str,
        pickup_time: str = None, delivery_date: str = None, pickup_date: str = None, 
        discount: float = None, extra_charges: List[ChargeDetails] = []):

        self.carrier = carrier
        self.service_name = service_name
        self.service_type = service_type
        self.base_charge = base_charge
        self.duties_and_taxes = duties_and_taxes
        self.total_charge = total_charge
        self.currency = currency
        self.discount = discount
        self.extra_charges = extra_charges

        self.pickup_time = pickup_time
        self.delivery_date = delivery_date
        self.pickup_date = pickup_date

class TrackingDetails:
    def __init__(self, carrier: str, tracking_number: str, shipment_date: str = None, events: List[TrackingEvent] = []): 
        self.carrier = carrier
        self.events = events
        self.shipment_date = shipment_date
        self.tracking_number = tracking_number

class ShipmentDetails:
    def __init__(self, carrier: str, tracking_numbers: List[str], total_charge: ChargeDetails, charges: List[ChargeDetails], shipment_date: str = None, 
        services: List[str] = None, documents: List[str] = [], reference: ReferenceDetails = None): 
        self.carrier = carrier
        self.tracking_numbers = tracking_numbers
        self.shipment_date = shipment_date
        self.documents = documents
        self.services = services
        self.reference = reference
        self.total_charge = total_charge
        self.charges = charges

class PickupDetails:
    def __init__(self, carrier: str, confirmation_number: str, pickup_date: str = None, 
        pickup_charge: ChargeDetails = None, ref_times: List[TimeDetails] = None): 
        self.carrier = carrier
        self.confirmation_number = confirmation_number
        self.pickup_date = pickup_date
        self.pickup_charge = pickup_charge
        self.ref_times = ref_times
