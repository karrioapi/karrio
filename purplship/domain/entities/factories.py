from collections import namedtuple
from typing import List, Dict
from purplship.domain.entities.datatypes import package_type, commodity_type, label_type, party, invoice_type

''' customs Type definition '''
class customs_details_type(namedtuple("customs_details_type", "no_eei aes description terms_of_trade items commercial_invoice extra")):
    def __new__(cls, no_eei: str = None, aes: str = None, description: str = None, terms_of_trade: str = None, items: List[dict] = [], commercial_invoice: bool = None, extra: dict = None):
        return super(cls, customs_details_type).__new__(
            cls, 
            no_eei,
            aes,
            description,
            terms_of_trade,
            [package_type(**i) for i in items],
            commercial_invoice,
            extra,
        )


''' quote options Type definition '''
class quote_options_type(namedtuple("quote_options_type", "packages insured_amount number_of_packages packaging_type is_document currency total_weight weight_unit dimension_unit paid_by declared_value duty_paid_by payment_country_code payment_account_number shipper_account_number services extra")):
    def __new__(cls, packages: List[package_type], insured_amount: float = None, number_of_packages: int = None, packaging_type: str = None, is_document: bool = False, currency: str = None, total_weight: float = None, weight_unit: str = "LB", dimension_unit: str = "IN", paid_by: str = None, declared_value: float = None, duty_paid_by: str = None, payment_country_code: str = None, payment_account_number: str = None, shipper_account_number: str = None, services: List[str] = [], extra: Dict = {}):
        return super(cls, quote_options_type).__new__(
            cls,
            [package_type(**p) for p in packages],
            insured_amount, 
            number_of_packages, 
            packaging_type, 
            is_document, 
            currency, 
            total_weight, 
            weight_unit, 
            dimension_unit, 
            paid_by, 
            declared_value,
            duty_paid_by,
            payment_country_code, 
            payment_account_number,
            shipper_account_number, 
            services,
            extra
        )


''' shipment options Type definition '''
class shipment_options_type(namedtuple("shipment_options_type", "packages insured_amount number_of_packages packaging_type is_document currency date total_weight weight_unit dimension_unit paid_by duty_paid_by payment_type payment_country_code duty_payment_account declared_value payment_account_number shipper_account_number billing_account_number services customs invoice references commodities label, extra")):
    def __new__(cls, packages: List, insured_amount: float = None, number_of_packages: int = None, packaging_type: str = None, is_document: bool = False, currency: str = None, date: str = None, total_weight: float = None, weight_unit: str = "LB", dimension_unit: str = "IN", paid_by: str = None, duty_paid_by: str = None, payment_type: str = None, payment_country_code: str = None, duty_payment_account: str = None, declared_value: float = None, payment_account_number: str = None, shipper_account_number: str = None, billing_account_number: str = None, services: List[str] = [], customs: Dict = None, invoice: dict = None, references: List[str] = [], commodities: List[Dict] = [], label: Dict = None, extra: Dict = {}):
        return super(cls, shipment_options_type).__new__(
            cls,
            [package_type(**p) for p in packages],
            insured_amount,
            number_of_packages,
            packaging_type,
            is_document,
            currency,
            date,
            total_weight,
            weight_unit,
            dimension_unit,
            paid_by,
            duty_paid_by,
            payment_type,
            payment_country_code,
            duty_payment_account,
            declared_value,
            payment_account_number,
            shipper_account_number,
            billing_account_number,
            services,
            customs_details_type(**customs) if customs else None,
            invoice_type(**invoice) if invoice else None,
            references,
            [commodity_type(**c) for c in commodities],
            label_type(**label) if label else None,
            extra
        )


''' quote request Type definition '''
class quote_request_type(namedtuple("quote_request_type", "shipper recipient shipment")):
    def __new__(cls, shipper: Dict, recipient: Dict, shipment: Dict):
        return super(cls, quote_request_type).__new__(
            cls, 
            party(**shipper), 
            party(**recipient), 
            quote_options_type(**shipment)
        )


''' shipment request Type definition '''
class shipment_request_type(namedtuple("shipment_request_type", "shipper recipient shipment")):
    def __new__(cls, shipper: Dict, recipient: Dict, shipment: Dict):
        return super(cls, shipment_request_type).__new__(
            cls, 
            party(**shipper), 
            party(**recipient), 
            shipment_options_type(**shipment)
        )

