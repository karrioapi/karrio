from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AttributesType:
    rate: Optional[float] = None
    maximum_cover: Optional[int] = None
    cover_amount: Optional[int] = None
    included_cover: Optional[int] = None


@s(auto_attribs=True)
class FeaturePriceType:
    calculated_price: Optional[float] = None
    calculated_price_ex_gst: Optional[float] = None
    calculated_gst: Optional[float] = None


@s(auto_attribs=True)
class FeatureType:
    type: Optional[str] = None
    attributes: Optional[AttributesType] = JStruct[AttributesType]
    price: Optional[FeaturePriceType] = JStruct[FeaturePriceType]
    bundled: Optional[bool] = None


@s(auto_attribs=True)
class FeaturesType:
    feature: Optional[FeatureType] = JStruct[FeatureType]


@s(auto_attribs=True)
class OptionsType:
    signature_on_delivery_option: Optional[bool] = None
    authority_to_leave_option: Optional[bool] = None


@s(auto_attribs=True)
class PriceElementType:
    product_id: Optional[str] = None
    product_type: Optional[str] = None
    options: Optional[OptionsType] = JStruct[OptionsType]
    calculated_price: Optional[float] = None
    calculated_price_ex_gst: Optional[float] = None
    calculated_gst: Optional[float] = None
    bundled_price: Optional[float] = None
    bundled_price_ex_gst: Optional[float] = None
    bundled_gst: Optional[float] = None
    features: Optional[FeaturesType] = JStruct[FeaturesType]
    calculated_gst_ex_gst: Optional[float] = None


@s(auto_attribs=True)
class WarningType:
    code: Optional[int] = None
    name: Optional[str] = None
    message: Optional[str] = None
    context: List[Any] = []


@s(auto_attribs=True)
class ItemType:
    weight: Optional[int] = None
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    prices: List[PriceElementType] = JList[PriceElementType]
    errors: List[Any] = []
    warnings: List[WarningType] = JList[WarningType]


@s(auto_attribs=True)
class RateResponseType:
    items: List[ItemType] = JList[ItemType]
