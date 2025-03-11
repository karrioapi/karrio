import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ComparisonType:
    changes: typing.Optional[str] = None
    post: typing.Optional[str] = None
    pre: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValidationType:
    detail: typing.Optional[str] = None
    status: typing.Optional[str] = None
    comparison: typing.Optional[ComparisonType] = jstruct.JStruct[ComparisonType]


@attr.s(auto_attribs=True)
class NAddressType:
    city: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    contact_email: typing.Optional[str] = None
    contact_name: typing.Optional[str] = None
    contact_phone: typing.Optional[str] = None
    country_alpha2: typing.Optional[str] = None
    line_1: typing.Optional[str] = None
    line_2: typing.Optional[str] = None
    postal_code: typing.Optional[str] = None
    state: typing.Optional[str] = None
    validation: typing.Optional[ValidationType] = jstruct.JStruct[ValidationType]


@attr.s(auto_attribs=True)
class ItemType:
    description: typing.Optional[str] = None
    quantity: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class TrackingRequestType:
    destination_address: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    origin_address: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    courier_id: typing.Optional[str] = None
    origin_address_id: typing.Optional[str] = None
    platform_order_number: typing.Optional[int] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    tracking_number: typing.Optional[int] = None
