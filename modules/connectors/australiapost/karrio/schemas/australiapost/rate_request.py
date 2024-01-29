from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AttributesType:
    cover_amount: Optional[float] = None


@s(auto_attribs=True)
class FeatureType:
    attributes: Optional[AttributesType] = JStruct[AttributesType]


@s(auto_attribs=True)
class FeaturesType:
    feature: Optional[FeatureType] = JStruct[FeatureType]


@s(auto_attribs=True)
class ItemType:
    item_reference: Optional[int] = None
    product_id: Optional[str] = None
    length: Optional[float] = None
    height: Optional[float] = None
    width: Optional[float] = None
    weight: Optional[float] = None
    packaging_type: Optional[str] = None
    product_ids: List[str] = []
    features: Optional[FeaturesType] = JStruct[FeaturesType]


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
