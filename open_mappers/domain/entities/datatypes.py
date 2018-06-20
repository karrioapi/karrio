from typing import List, NamedTuple
import json

class contact_type(NamedTuple):
    company_name: str = None
    person_name: str = None
    phone_number: str = None
    email_address: str = None

class address_type(NamedTuple):
    country_code: str
    state_or_province: str = None
    country_name: str = None
    postal_code: str = None
    city: str = None
    address_lines: List[str] = []

class package_type(NamedTuple):
    width: float
    height: float
    lenght: float
    weight: float
    id: str = None
    packaging_type: str = None
    description: str = None

class charges_payment_type(NamedTuple):
    type: str
    account_number: str

class insurance_type(NamedTuple):
    value: str
    currency: str

class party(NamedTuple):
    address: address_type
    contact: contact_type = None


class shipment_details(NamedTuple):
    packages: List[package_type]
    insurance: insurance_type = None 
    charges_payment: charges_payment_type = None 
    number_of_packages: int = None
    packaging_type: str = None
    is_dutiable: str = "N"
    currency: str = None
    total_weight: float = None
    weight_unit: str = "LB"
    dimension_unit: str = "IN"

class quote_request(NamedTuple):
    shipper: party 
    recipient: party
    shipment_details: shipment_details





def jsonify(entity): 
    return json.dumps(entity, default=lambda o: o.__dict__, sort_keys=True, indent=4)