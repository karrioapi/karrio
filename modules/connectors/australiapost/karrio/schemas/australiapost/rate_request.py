from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ItemType:
    product_id: Optional[str] = None
    length: Optional[int] = None
    height: Optional[int] = None
    width: Optional[int] = None
    weight: Optional[int] = None


@s(auto_attribs=True)
class FromType:
    suburb: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[int] = None


@s(auto_attribs=True)
class ShipmentType:
    shipment_from: Optional[FromType] = JStruct[FromType]
    to: Optional[FromType] = JStruct[FromType]
    items: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class RateRequestType:
    shipments: List[ShipmentType] = JList[ShipmentType]
