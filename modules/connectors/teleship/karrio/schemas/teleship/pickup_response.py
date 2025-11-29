import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MessageType:
    code: typing.Optional[int] = None
    level: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    message: typing.Optional[str] = None
    details: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class AddressAddressType:
    line1: typing.Optional[str] = None
    line2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postcode: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupAddressType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address: typing.Optional[AddressAddressType] = jstruct.JStruct[AddressAddressType]


@attr.s(auto_attribs=True)
class PickupType:
    id: typing.Optional[str] = None
    status: typing.Optional[str] = None
    startAt: typing.Optional[str] = None
    endAt: typing.Optional[str] = None
    address: typing.Optional[PickupAddressType] = jstruct.JStruct[PickupAddressType]
    reference: typing.Optional[str] = None
    createdAt: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupResponseType:
    messages: typing.Optional[typing.List[MessageType]] = jstruct.JList[MessageType]
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
