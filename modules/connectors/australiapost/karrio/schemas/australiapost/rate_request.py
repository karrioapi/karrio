from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AttributesType:
    cover_amount: Optional[float] = None


@s(auto_attribs=True)
class TransitCoverType:
    attributes: Optional[AttributesType] = JStruct[AttributesType]


@s(auto_attribs=True)
class FeaturesType:
    TRANSIT_COVER: Optional[TransitCoverType] = JStruct[TransitCoverType]


@s(auto_attribs=True)
class ItemType:
    item_reference: Optional[str] = None
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
    postcode: Optional[int] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class RateRequestType:
    rate_request_from: Optional[FromType] = JStruct[FromType]
    to: Optional[FromType] = JStruct[FromType]
    items: List[ItemType] = JList[ItemType]
