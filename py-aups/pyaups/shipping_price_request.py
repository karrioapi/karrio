"""Australia Post Price Datatype definition module."""

import attr
from typing import List
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class TrackingDetails:
    article_id: str = None
    barcode_id: str = None
    consignment_id: str = None


@attr.s(auto_attribs=True)
class ItemContent:
    description: str = None
    quantity: str = None
    weight: float = None
    value: float = None
    tariff_code: str = None
    country_of_origin: str = None


@attr.s(auto_attribs=True)
class Item:
    item_reference: str = None
    product_id: str = None
    item_description: str = None
    length: float = None
    width: float = None
    height: float = None
    cubic_volume: float = None
    weight: float = None
    contains_dangerous_goods: bool = None
    transportable_by_air: bool = None
    dangerous_goods_declaration: str = None
    authority_to_leave: bool = None
    reason_for_return: str = None
    allow_partial_delivery: bool = None
    packaging_type: str = None
    atl_number: str = None
    features: dict = None
    tracking_details: TrackingDetails = JStruct[TrackingDetails]
    commercial_value: bool = None
    export_declaration_number: str = None
    import_reference_number: str = None
    classification_type: str = None
    description_of_other: str = None
    international_parcel_sender_name: str = None
    non_delivery_action: str = None
    certificate_number: str = None
    licence_number: str = None
    invoice_number: str = None
    comments: str = None
    item_contents: List[ItemContent] = JList[ItemContent]
    tariff_concession: str = None
    free_trade_applicable: bool = None


@attr.s(auto_attribs=True)
class DangerousGood:
    un_number: str = None
    technical_name: str = None
    net_weight: str = None
    class_division: str = None
    subsidiary_risk: str = None
    packing_group_designator: str = None
    outer_packaging_type: str = None
    outer_packaging_quantity: str = None


@attr.s(auto_attribs=True)
class From:
    name: str = None
    type: str = None
    lines: List[str] = []
    suburb: str = None
    state: str = None
    postcode: str = None
    country: str = None
    phone: str = None
    email: str = None


@attr.s(auto_attribs=True)
class To:
    name: str = None
    apcn: str = None
    business_name: str = None
    type: str = None
    lines: List[str] = []
    suburb: str = None
    state: str = None
    postcode: str = None
    country: str = None
    phone: str = None
    email: str = None
    delivery_instructions: str = None


@attr.s(auto_attribs=True)
class Shipment:
    shipment_reference: str = None
    sender_references: List[str] = []
    goods_descriptions: List[str] = []
    despatch_date: str = None
    consolidate: bool = None
    email_tracking_enabled: bool = None
    from_: From = JStruct[From]
    to: To = JStruct[To]
    dangerous_goods: DangerousGood = JStruct[DangerousGood]
    movement_type: str = None
    features: dict = None
    authorisation_number: str = None
    items: List[Item] = JList[Item]


@attr.s(auto_attribs=True)
class ShippingPriceRequest:
    shipments: List[Shipment] = JList[Shipment]
