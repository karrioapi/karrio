import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressAddressType:
    line1: typing.Optional[str] = None
    line2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postcode: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupRequestAddressType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address: typing.Optional[AddressAddressType] = jstruct.JStruct[AddressAddressType]


@attr.s(auto_attribs=True)
class PickupRequestType:
    startAt: typing.Optional[str] = None
    endAt: typing.Optional[str] = None
    shipmentIds: typing.Optional[typing.List[str]] = None
    address: typing.Optional[PickupRequestAddressType] = jstruct.JStruct[PickupRequestAddressType]
    reference: typing.Optional[str] = None
