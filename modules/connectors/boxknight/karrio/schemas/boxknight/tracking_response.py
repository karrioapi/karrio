import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Location:
    lat: typing.Optional[float] = None
    lng: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Address:
    number: typing.Optional[int] = None
    street: typing.Optional[str] = None
    city: typing.Optional[str] = None
    province: typing.Optional[str] = None
    country: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    sublocality: typing.Optional[str] = None
    location: typing.Optional[Location] = jstruct.JStruct[Location]


@attr.s(auto_attribs=True)
class Recipient:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    notes: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    id: typing.Optional[str] = None
    createdAt: typing.Optional[str] = None
    createdBy: typing.Optional[str] = None
    merchantId: typing.Optional[str] = None
    orderStatus: typing.Optional[str] = None
    scanningRequired: typing.Optional[bool] = None
    validAddress: typing.Optional[bool] = None
    labelUrl: typing.Optional[str] = None
    pdfLabelUrl: typing.Optional[str] = None
    recipient: typing.Optional[Recipient] = jstruct.JStruct[Recipient]
    recipientAddress: typing.Optional[Address] = jstruct.JStruct[Address]
    originAddress: typing.Optional[Address] = jstruct.JStruct[Address]
    packageCount: typing.Optional[int] = None
    signatureRequired: typing.Optional[bool] = None
    service: typing.Optional[str] = None
    notes: typing.Optional[str] = None
    refNumber: typing.Optional[str] = None
    completeAfter: typing.Optional[int] = None
    completeBefore: typing.Optional[int] = None
    merchantDisplayName: typing.Optional[str] = None
