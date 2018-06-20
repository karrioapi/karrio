from .datatypes import *
from ..entities import *
from collections import namedtuple

''' ShipmentDetails Type definition '''
class shipment_details_type(namedtuple("shipment_details_type", "packages insurance charges_payment number_of_packages packaging_type is_dutiable currency total_weight weight_unit dimension_unit")):
    def __new__(cls, packages, insurance=None, charges_payment=None, number_of_packages=None, packaging_type=None, is_dutiable="N", currency=None, total_weight=None, weight_unit="LB", dimension_unit="IN"):
        return super(cls, shipment_details_type).__new__(
            cls,
            list(map(lambda p: package_type(**p), packages)),
            insurance if insurance is None else insurance_type(**insurance),
            charges_payment if charges_payment is None else charges_payment_type(**charges_payment),
            number_of_packages, packaging_type, is_dutiable, currency, total_weight, weight_unit, dimension_unit
        )


''' quote_request Type definition '''
class quote_request_type(namedtuple("quote_request_type", "shipper recipient shipment_details")):
    def __new__(cls, shipper, recipient, shipment_details):
        return super(cls, quote_request_type).__new__(
            cls, 
            Party.create(**shipper), 
            Party.create(**recipient), 
            ShipmentDetails.create(**shipment_details)
        )




''' Party Type definition '''
class party_type(namedtuple("party_type", "address contact")):
    def __new__(cls, address, contact=None):
        return super(cls, party_type).__new__(
            cls, 
            address_type(**address), 
            contact if contact is None else contact_type(**contact)
        )