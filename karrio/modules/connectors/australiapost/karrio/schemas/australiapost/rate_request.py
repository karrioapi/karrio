import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ItemType:
    item_reference: typing.Optional[str] = None
    product_id: typing.Optional[str] = None
    length: typing.Optional[float] = None
    height: typing.Optional[float] = None
    width: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    packaging_type: typing.Optional[str] = None
    product_ids: typing.Optional[typing.List[str]] = None
    features: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class FromType:
    postcode: typing.Optional[int] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateRequestType:
    rate_request_from: typing.Optional[FromType] = jstruct.JStruct[FromType]
    to: typing.Optional[FromType] = jstruct.JStruct[FromType]
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
