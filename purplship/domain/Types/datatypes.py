from typing import List, NamedTuple, Dict

class party(NamedTuple):
    postal_code: str = None
    city: str = None
    type: str = None
    tax_id: str = None
    account_number: str = None
    person_name: str = None
    company_name: str = None
    country_name: str = None
    country_code: str = None
    email_address: str = None
    phone_number: str = None

    """ state or province """
    state: str = None
    state_code: str = None

    address_lines: List[str] = []
    extra: Dict = {}

class item_type(NamedTuple):
    """
        item type is a package of commodity
    """

    weight: float
    id: str = None
    width: float = None
    height: float = None
    length: float = None
    packaging_type: str = None
    description: str = None
    content: str = None
    quantity: int = 1
    sku: str = None
    code: str = None
    value_amount: float = None
    value_currency: str = None
    origin_country: str = None
    extra: Dict = {}

class customs_type(NamedTuple):
    no_eei: str = None
    aes: str = None
    description: str = None
    terms_of_trade: str = None
    items: List[item_type] = []
    commercial_invoice: bool = False
    extra: Dict = {}

class invoice_type(NamedTuple):
    date: str
    identifier: str = None
    type: str = None
    copies: int = None
    extra: Dict = {}

class doc_image(NamedTuple):
    type: str = None
    format: str = None
    image: str = None
    extra: Dict = {}

class option_type(NamedTuple):
    code: str 
    value: Dict = {}
    extra: Dict = {}

class shipment_options(NamedTuple):

    """ packages or commodities """
    items: List[item_type]

    insured_amount: float = None
    total_items: int = None
    packaging_type: str = None
    is_document: bool = False
    total_weight: float = None
    weight_unit: str = "LB"
    dimension_unit: str = "IN"

    currency: str = None
    paid_by: str = None
    declared_value: float = None
    payment_type: str = None
    duty_paid_by: str = None
    duty_payment_account: str = None
    payment_country_code: str = None
    payment_account_number: str = None

    ship_date: str = None
    customs: customs_type = None
    invoice: invoice_type = None
    doc_images: List[doc_image] = []
    
    references: List[str] = []
    services: List[str] = []
    options: List[option_type] = []

    label: doc_image = None
    extra: Dict = {}

class shipment_request(NamedTuple):
    shipper: party 
    recipient: party
    shipment: shipment_options

class tracking_request(NamedTuple):
    tracking_numbers: List[str]
    language_code: str = None
    level_of_details: str = None
    extra: Dict = {}

class pickup_request(NamedTuple):
    date: str
    account_number: str
    weight: float = None
    weight_unit: str = None
    pieces: float = None
    ready_time: str = None
    closing_time: str = None
    instruction: str = None
    package_location: str = None

    city: str = None
    postal_code: str = None
    person_name: str = None
    company_name: str = None
    phone_number: str = None
    email_address: str = None
    is_business: bool = True

    """ state or province """
    state: str = None
    state_code: str = None

    country_name: str = None
    country_code: str = None

    """ required for pickup modification """
    confirmation_number: str = None

    address_lines: List[str] = []
    extra: Dict = {}   

class pickup_cancellation_request(NamedTuple):
    pickup_date: str
    confirmation_number: str
    person_name: str = None
    country_code: str = None
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
