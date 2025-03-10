import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Address:
    street: typing.Optional[str] = None
    unit: typing.Optional[str] = None
    city: typing.Optional[str] = None
    province: typing.Optional[str] = None
    country: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    isBusinessAddress: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class SizeOptions:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightOptions:
    weight: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Package:
    refNumber: typing.Optional[int] = None
    weightOptions: typing.Optional[WeightOptions] = jstruct.JStruct[WeightOptions]
    sizeOptions: typing.Optional[SizeOptions] = jstruct.JStruct[SizeOptions]


@attr.s(auto_attribs=True)
class Recipient:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    notes: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderRequest:
    recipient: typing.Optional[Recipient] = jstruct.JStruct[Recipient]
    recipientAddress: typing.Optional[Address] = jstruct.JStruct[Address]
    originAddress: typing.Optional[Address] = jstruct.JStruct[Address]
    packageCount: typing.Optional[int] = None
    service: typing.Optional[str] = None
    notes: typing.Optional[str] = None
    refNumber: typing.Optional[str] = None
    merchantDisplayName: typing.Optional[str] = None
    signatureRequired: typing.Optional[bool] = None
    packages: typing.Optional[typing.List[Package]] = jstruct.JList[Package]
