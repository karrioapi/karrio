"""Australia Post Price Datatype definition module."""

import attr
from typing import List
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class ShipmentSummary:
    total_cost: float = None
    total_cost_ex_gst: float = None
    total_gst: float = None
    status: str = None
    number_of_items: int = None
    tracking_summary: List[str] = None
    freight_charge: float = None
    discount: float = None
    transit_cover: float = None
    security_surcharge: float = None
    fuel_surcharge: float = None


@attr.s(auto_attribs=True)
class From:
    type_: str = None
    lines: str = None
    suburb: str = None
    postcode: str = None
    state: str = None
    name: str = None
    email: str = None
    phone: str = None


@attr.s(auto_attribs=True)
class To:
    type_: str = None
    lines: str = None
    suburb: str = None
    postcode: str = None
    state: str = None
    name: str = None
    apcn: str = None
    business_name: str = None
    email: str = None
    phone: str = None
    delivery_instructions: str = None


@attr.s(auto_attribs=True)
class Item:
    height: float = None
    length: float = None
    width: float = None
    weight: float = None
    packaging_type: str = None
    atl_number: str = None


@attr.s(auto_attribs=True)
class Shipment:
    shipment_id: str = None
    shipment_reference: str = None
    shipment_creation_date: str = None
    email_tracking_enabled: str = None
    from_: From = None
    to: To = None
    items: List[Item] = JList[Item]
    shipment_summary: ShipmentSummary = JStruct[ShipmentSummary]


@attr.s(auto_attribs=True)
class Error:
    code: str = None
    name: str = None
    message: str = None
    field: str = None
    context: dict = None


@attr.s(auto_attribs=True)
class ShippingPriceResponse:
    shipments: List[Shipment] = JList[Shipment]
    errors: List[Error] = JList[Error]


@attr.s(auto_attribs=True)
class Errors:
    errors: List[Error] = JList[Error]
