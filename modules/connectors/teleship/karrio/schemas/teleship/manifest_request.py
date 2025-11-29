import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressAddressType:
    line1: typing.Optional[str] = None
    line2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postcode: typing.Optional[int] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ManifestRequestAddressType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address: typing.Optional[AddressAddressType] = jstruct.JStruct[AddressAddressType]


@attr.s(auto_attribs=True)
class MessageType:
    code: typing.Optional[int] = None
    level: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    message: typing.Optional[str] = None
    details: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ManifestRequestType:
    messages: typing.Optional[typing.List[MessageType]] = jstruct.JList[MessageType]
    shipmentIds: typing.Optional[typing.List[str]] = None
    reference: typing.Optional[str] = None
    address: typing.Optional[ManifestRequestAddressType] = jstruct.JStruct[ManifestRequestAddressType]
