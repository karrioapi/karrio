from collections import namedtuple
from typing import List, Dict
from purplship.domain.Types.datatypes import (
    item_type,
    party,
    invoice_type,
    doc_image,
    option_type,
    shipment_options,
    customs_type,
)


def create_customs_type(
    no_eei: str = None,
    aes: str = None,
    description: str = None,
    terms_of_trade: str = None,
    items: List[dict] = [],
    commercial_invoice: bool = False,
    extra: dict = {},
) -> customs_type:
    """ customs Type factory function """
    return customs_type(
        no_eei=no_eei,
        aes=aes,
        description=description,
        terms_of_trade=terms_of_trade,
        items=[item_type(**i) for i in items],
        commercial_invoice=commercial_invoice,
        extra=extra,
    )


def create_shipment_options(
    items: List,
    insured_amount: float = None,
    total_items: int = None,
    packaging_type: str = None,
    is_document: bool = False,
    currency: str = None,
    total_weight: float = None,
    weight_unit: str = "LB",
    dimension_unit: str = "IN",
    paid_by: str = None,
    duty_paid_by: str = None,
    payment_type: str = None,
    payment_country_code: str = None,
    duty_payment_account: str = None,
    declared_value: float = None,
    payment_account_number: str = None,
    services: List[str] = [],
    options: List[dict] = [],
    date: str = None,
    customs: dict = None,
    invoice: dict = None,
    doc_images: List[dict] = [],
    references: List[str] = [],
    label: Dict = None,
    extra: Dict = {},
) -> shipment_options:
    """ shipment options Type factory function """
    return shipment_options(
        items=[item_type(**p) for p in items],
        insured_amount=insured_amount,
        total_items=total_items,
        packaging_type=packaging_type,
        is_document=is_document,
        currency=currency,
        total_weight=total_weight,
        weight_unit=weight_unit,
        dimension_unit=dimension_unit,
        paid_by=paid_by,
        duty_paid_by=duty_paid_by,
        payment_type=payment_type,
        payment_country_code=payment_country_code,
        duty_payment_account=duty_payment_account,
        declared_value=declared_value,
        payment_account_number=payment_account_number,
        services=services,
        options=[option_type(**option) for option in options],
        date=date,
        customs=create_customs_type(**customs) if customs else None,
        invoice=invoice_type(**invoice) if invoice else None,
        doc_images=[doc_image(**doc) for doc in doc_images],
        references=references,
        label=doc_image(**label) if label else None,
        extra=extra,
    )
