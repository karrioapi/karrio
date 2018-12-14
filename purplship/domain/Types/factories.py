from collections import namedtuple
from typing import List, Dict
from purplship.domain.Types.datatypes import item_type, party, invoice_type, doc_image, option_type

''' customs Type definition '''
class customs_details_type(namedtuple("customs_details_type", "no_eei aes description terms_of_trade items commercial_invoice extra")):
    def __new__(cls, no_eei: str = None, aes: str = None, description: str = None, terms_of_trade: str = None, items: List[dict] = [], commercial_invoice: bool = None, extra: dict = None):
        return super(cls, customs_details_type).__new__(
            cls, 
            no_eei,
            aes,
            description,
            terms_of_trade,
            [item_type(**i) for i in items],
            commercial_invoice,
            extra,
        )


''' shipment options Type definition '''
class shipment_options_type(namedtuple("shipment_options_type", "items insured_amount total_items packaging_type is_document currency date total_weight weight_unit dimension_unit paid_by duty_paid_by payment_type payment_country_code duty_payment_account declared_value payment_account_number billing_account_number services options customs invoice doc_images references label, extra")):
    def __new__(cls, items: List, insured_amount: float = None, total_items: int = None, packaging_type: str = None, is_document: bool = False, currency: str = None, date: str = None, total_weight: float = None, weight_unit: str = "LB", dimension_unit: str = "IN", paid_by: str = None, duty_paid_by: str = None, payment_type: str = None, payment_country_code: str = None, duty_payment_account: str = None, declared_value: float = None, payment_account_number: str = None, billing_account_number: str = None, services: List[str] = [], options: List[dict] = [], customs: Dict = None, invoice: dict = None, doc_images: List[dict] = [], references: List[str] = [], label: Dict = None, extra: Dict = {}):
        return super(cls, shipment_options_type).__new__(
            cls,
            [item_type(**p) for p in items],
            insured_amount,
            total_items,
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
            billing_account_number,
            services,
            [option_type(**option) for option in options],
            customs_details_type(**customs) if customs else None,
            invoice_type(**invoice) if invoice else None,
            [doc_image(**doc) for doc in doc_images],
            references,
            doc_image(**label) if label else None,
            extra
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

