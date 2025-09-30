import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AttributesType:
    rate: typing.Optional[float] = None
    maximum_cover: typing.Optional[int] = None
    cover_amount: typing.Optional[int] = None
    included_cover: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class FeaturePriceType:
    calculated_price: typing.Optional[float] = None
    calculated_price_ex_gst: typing.Optional[float] = None
    calculated_gst: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class FeatureType:
    type: typing.Optional[str] = None
    attributes: typing.Optional[AttributesType] = jstruct.JStruct[AttributesType]
    price: typing.Optional[FeaturePriceType] = jstruct.JStruct[FeaturePriceType]
    bundled: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class FeaturesType:
    feature: typing.Optional[FeatureType] = jstruct.JStruct[FeatureType]


@attr.s(auto_attribs=True)
class OptionsType:
    signature_on_delivery_option: typing.Optional[bool] = None
    authority_to_leave_option: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class PriceElementType:
    product_id: typing.Optional[str] = None
    product_type: typing.Optional[str] = None
    options: typing.Optional[OptionsType] = jstruct.JStruct[OptionsType]
    calculated_price: typing.Optional[float] = None
    calculated_price_ex_gst: typing.Optional[float] = None
    calculated_gst: typing.Optional[float] = None
    bundled_price: typing.Optional[float] = None
    bundled_price_ex_gst: typing.Optional[float] = None
    bundled_gst: typing.Optional[float] = None
    features: typing.Optional[FeaturesType] = jstruct.JStruct[FeaturesType]
    calculated_gst_ex_gst: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class WarningType:
    code: typing.Optional[int] = None
    name: typing.Optional[str] = None
    message: typing.Optional[str] = None
    context: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class ItemType:
    weight: typing.Optional[int] = None
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    prices: typing.Optional[typing.List[PriceElementType]] = jstruct.JList[PriceElementType]
    errors: typing.Optional[typing.List[typing.Any]] = None
    warnings: typing.Optional[typing.List[WarningType]] = jstruct.JList[WarningType]


@attr.s(auto_attribs=True)
class RateResponseType:
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
