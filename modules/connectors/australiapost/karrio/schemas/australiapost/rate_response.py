from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class FeaturesType:
    pass


@s(auto_attribs=True)
class ItemType:
    weight: Optional[int] = None
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    product_id: Optional[str] = None


@s(auto_attribs=True)
class FromType:
    type: Optional[str] = None
    lines: List[Any] = []
    suburb: Optional[str] = None
    postcode: Optional[int] = None
    state: Optional[str] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class ShipmentSummaryType:
    total_cost: Optional[float] = None
    total_cost_ex_gst: Optional[float] = None
    shipping_cost: Optional[float] = None
    fuel_surcharge: Optional[float] = None
    total_gst: Optional[float] = None
    tracking_summary: Optional[FeaturesType] = JStruct[FeaturesType]
    number_of_items: Optional[int] = None


@s(auto_attribs=True)
class ShipmentType:
    shipment_from: Optional[FromType] = JStruct[FromType]
    to: Optional[FromType] = JStruct[FromType]
    items: List[ItemType] = JList[ItemType]
    options: Optional[FeaturesType] = JStruct[FeaturesType]
    features: Optional[FeaturesType] = JStruct[FeaturesType]
    shipment_summary: Optional[ShipmentSummaryType] = JStruct[ShipmentSummaryType]
    movement_type: Optional[str] = None
    charge_to_account: Optional[str] = None


@s(auto_attribs=True)
class RateResponseType:
    shipments: List[ShipmentType] = JList[ShipmentType]
