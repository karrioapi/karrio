from typing import List, NamedTuple, Dict

class party(NamedTuple):
    postal_code: str = None
    city: str = None
    type: str = None
    tax_id: str = None
    person_name: str = None
    company_name: str = None
    country_name: str = None
    country_code: str = None
    email_address: str = None
    phone_number: str = None
    state_or_province: str = None
    state_or_province_code: str = None
    address_lines: List[str] = []
    extra: Dict = {}

class package_type(NamedTuple):
    weight: float
    width: float = None
    height: float = None
    length: float = None
    id: str = None
    packaging_type: str = None
    description: str = None
    extra: Dict = {}

class customs_type(NamedTuple):
    description: str = None
    terms_of_trade: str = None
    extra: Dict = {}

class commodity_type(NamedTuple):
    code: str = None
    description: str = None
    extra: Dict = {}

class label_type(NamedTuple):
    format: str = None
    type: str = None
    extra: Dict = None

class quote_options(NamedTuple):
    packages: List[package_type]
    insured_amount: float = None
    number_of_packages: int = None
    packaging_type: str = None
    is_document: bool = False
    currency: str = None
    total_weight: float = None
    weight_unit: str = "LB"
    dimension_unit: str = "IN"
    paid_by: str = None
    payment_country_code: str = None
    payment_account_number: str = None
    shipper_account_number: str = None
    services: List[str] = []
    extra: Dict = {}

class shipment_options(NamedTuple):
    packages: List[package_type]
    insured_amount: float = None
    number_of_packages: int = None
    packaging_type: str = None
    is_document: bool = False
    currency: str = None
    date: str = None
    total_weight: float = None
    weight_unit: str = "LB"
    dimension_unit: str = "IN"
    paid_by: str = None
    duty_paid_by: str = None
    duty_payment_account: str = None
    declared_value: float = None
    payment_country_code: str = None
    payment_account_number: str = None
    shipper_account_number: str = None
    billing_account_number: str = None
    services: List[str] = []
    customs: customs_type = None
    references: List[str] = []
    commodities: List[commodity_type] = []
    label: label_type = None
    extra: Dict = {}

class quote_request(NamedTuple):
    shipper: party 
    recipient: party
    shipment: quote_options

class shipment_request(NamedTuple):
    shipper: party 
    recipient: party
    shipment: shipment_options

class tracking_request(NamedTuple):
    tracking_numbers: List[str]
    language_code: str = None
    level_of_details: str = None


''' Generic response data types '''

class Charge:
    def __init__(self, name: str = None, amount: str = None, currency: str = None):
        self.name = name
        self.amount = amount
        self.currency = currency

class Reference:
    def __init__(self, value: str, type: str = None):
        self.value = value
        self.type = type

class TrackingEvent:
    def __init__(self, date: str, description: str, location: str, code: str, time: str = None, signatory: str = None):
        self.date = date
        self.time = time
        self.description = description
        self.location = location
        self.code = code
        self.signatory = signatory

class quote_details:
    def __init__(self, carrier: str, service_name: str, service_type: str, 
        base_charge: float, duties_and_taxes: float, total_charge: float, 
        delivery_time: str = None, pickup_time: str = None, delivery_date: str = None, 
        pickup_date: str = None, discount: float = None, extra_charges: List[Charge] = []):

        self.carrier = carrier
        self.service_name = service_name
        self.service_type = service_type
        self.base_charge = base_charge
        self.duties_and_taxes = duties_and_taxes
        self.total_charge = total_charge
        self.discount = discount
        self.extra_charges = extra_charges

        self.delivery_time = delivery_time
        self.pickup_time = pickup_time
        self.delivery_date = delivery_date
        self.pickup_date = pickup_date


class tracking_details():
    def __init__(self, carrier: str, tracking_number: str, shipment_date: str = None, events: List[TrackingEvent] = []): 
        self.carrier = carrier
        self.events = events
        self.shipment_date = shipment_date
        self.tracking_number = tracking_number


class shipment_details():
    def __init__(self, carrier: str, tracking_number: str, total_charge: Charge, shipment_date: str = None, 
        service: str = None, documents: List[str] = [], reference: Reference = None): 
        self.carrier = carrier
        self.tracking_number = tracking_number
        self.shipment_date = shipment_date
        self.documents = documents
        self.service = service
        self.reference = reference
        self.total_charge = total_charge