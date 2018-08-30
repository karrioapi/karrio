from collections import namedtuple
from typing import List
from openship.domain.entities.datatypes import package_type, commodity_type, customs_type, label_type, party

''' quote options Type definition '''
class quote_options_type(namedtuple("quote_options_type", "packages insured_amount number_of_packages packaging_type is_document currency total_weight weight_unit dimension_unit paid_by payment_country_code payment_account_number shipper_account_number services")):
    def __new__(cls, packages: List[package_type], insured_amount: float = None, number_of_packages: int = None, packaging_type: str = None, is_document: bool = False, currency: str = None, total_weight: float = None, weight_unit: str = "LB", dimension_unit: str = "IN", paid_by: str = None, payment_country_code: str = None, payment_account_number: str = None, shipper_account_number: str = None, services: List[str] = []):
        return super(cls, quote_options_type).__new__(
            cls,
            list(map(lambda p: package_type(**p), packages)),
            insured_amount, 
            number_of_packages, 
            packaging_type, 
            is_document, 
            currency, 
            total_weight, 
            weight_unit, 
            dimension_unit, 
            paid_by, 
            payment_country_code, 
            payment_account_number,
            shipper_account_number, 
            services
        )

''' shipment options Type definition '''
class shipment_options_type(namedtuple("shipment_options_type", "packages insured_amount number_of_packages packaging_type is_document currency total_weight weight_unit dimension_unit paid_by duty_paid_by payment_country_code duty_payment_account payment_account_number shipper_account_number billing_account_number services customs references commodities label")):
    def __new__(cls, packages: List[package_type], insured_amount: float = None, number_of_packages: int = None, packaging_type: str = None, is_document: bool = False, currency: str = None, total_weight: float = None, weight_unit: str = "LB", dimension_unit: str = "IN", paid_by: str = None, duty_paid_by: str = None, payment_country_code: str = None, duty_payment_account: str = None, payment_account_number: str = None, shipper_account_number: str = None, billing_account_number: str = None, services: List[str] = [], customs: customs_type = None, references: List[str] = [], commodities: List[commodity_type] = [], label: label_type = None):
        return super(cls, shipment_options_type).__new__(
            cls,
            list(map(lambda p: package_type(**p), packages)),
            insured_amount,
            number_of_packages,
            packaging_type,
            is_document,
            currency,
            total_weight,
            weight_unit,
            dimension_unit,
            paid_by,
            duty_paid_by,
            payment_country_code,
            duty_payment_account,
            payment_account_number,
            shipper_account_number,
            billing_account_number,
            services,
            customs_type(**customs),
            references,
            list(map(lambda c: commodity_type(**c), commodities)),
            label_type(**label)
        )


''' quote request Type definition '''
class quote_request_type(namedtuple("quote_request_type", "shipper recipient shipment")):
    def __new__(cls, shipper, recipient, shipment):
        return super(cls, quote_request_type).__new__(
            cls, 
            party(**shipper), 
            party(**recipient), 
            quote_options_type(**shipment)
        )


''' shipment request Type definition '''
class shipment_request_type(namedtuple("shipment_request_type", "shipper recipient shipment")):
    def __new__(cls, shipper, recipient, shipment):
        return super(cls, shipment_request_type).__new__(
            cls, 
            party(**shipper), 
            party(**recipient), 
            shipment_options_type(**shipment)
        )