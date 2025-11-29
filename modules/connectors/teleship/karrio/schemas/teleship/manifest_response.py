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
class ManifestResponseAddressType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address: typing.Optional[AddressAddressType] = jstruct.JStruct[AddressAddressType]


@attr.s(auto_attribs=True)
class ManifestResponseType:
    id: typing.Optional[str] = None
    status: typing.Optional[str] = None
    reference: typing.Optional[str] = None
    createdAt: typing.Optional[str] = None
    address: typing.Optional[ManifestResponseAddressType] = jstruct.JStruct[ManifestResponseAddressType]
