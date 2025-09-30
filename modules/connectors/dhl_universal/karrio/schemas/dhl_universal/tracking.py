import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Error:
    title: typing.Optional[str] = None
    detail: typing.Optional[str] = None
    status: typing.Optional[int] = None
    instance: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingRequest:
    trackingNumber: typing.Optional[str] = None
    service: typing.Optional[str] = None
    requesterCountryCode: typing.Optional[str] = None
    originCountryCode: typing.Optional[str] = None
    recipientPostalCode: typing.Optional[str] = None
    language: typing.Optional[str] = None
    offset: typing.Optional[int] = None
    limit: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class Address:
    countryCode: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    addressLocality: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Destination:
    address: typing.Optional[Address] = jstruct.JStruct[Address]


@attr.s(auto_attribs=True)
class Carrier:
    type: typing.Optional[str] = None
    organizationName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Weight:
    value: typing.Optional[float] = None
    unitText: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Dimensions:
    width: typing.Optional[Weight] = jstruct.JStruct[Weight]
    height: typing.Optional[Weight] = jstruct.JStruct[Weight]
    length: typing.Optional[Weight] = jstruct.JStruct[Weight]


@attr.s(auto_attribs=True)
class Product:
    productName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Receiver:
    type: typing.Optional[str] = None
    familyName: typing.Optional[str] = None
    givenName: typing.Optional[str] = None
    name: typing.Optional[str] = None
    organizationName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ProofOfDelivery:
    timestamp: typing.Optional[str] = None
    signatureUrl: typing.Optional[str] = None
    documentUrl: typing.Optional[str] = None
    signed: typing.Optional[Receiver] = jstruct.JStruct[Receiver]


@attr.s(auto_attribs=True)
class References:
    number: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Volume:
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class Details:
    carrier: typing.Optional[Carrier] = jstruct.JStruct[Carrier]
    product: typing.Optional[Product] = jstruct.JStruct[Product]
    receiver: typing.Optional[Receiver] = jstruct.JStruct[Receiver]
    sender: typing.Optional[Receiver] = jstruct.JStruct[Receiver]
    proofOfDelivery: typing.Optional[ProofOfDelivery] = jstruct.JStruct[ProofOfDelivery]
    totalNumberOfPieces: typing.Optional[int] = None
    pieceIds: typing.Optional[typing.List[str]] = None
    weight: typing.Optional[Weight] = jstruct.JStruct[Weight]
    volume: typing.Optional[Volume] = jstruct.JStruct[Volume]
    loadingMeters: typing.Optional[float] = None
    dimensions: typing.Optional[Dimensions] = jstruct.JStruct[Dimensions]
    references: typing.Optional[References] = jstruct.JStruct[References]


@attr.s(auto_attribs=True)
class EstimatedDeliveryTimeFrame:
    estimatedFrom: typing.Optional[str] = None
    estimatedThrough: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Status:
    timestamp: typing.Optional[str] = None
    location: typing.Optional[Destination] = jstruct.JStruct[Destination]
    statusCode: typing.Optional[str] = None
    status: typing.Optional[str] = None
    description: typing.Optional[str] = None
    remark: typing.Optional[str] = None
    nextSteps: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Shipment:
    id: typing.Optional[int] = None
    service: typing.Optional[str] = None
    origin: typing.Optional[Destination] = jstruct.JStruct[Destination]
    destination: typing.Optional[Destination] = jstruct.JStruct[Destination]
    status: typing.Optional[Status] = jstruct.JStruct[Status]
    estimatedTimeOfDelivery: typing.Optional[str] = None
    estimatedDeliveryTimeFrame: typing.Optional[EstimatedDeliveryTimeFrame] = jstruct.JStruct[EstimatedDeliveryTimeFrame]
    estimatedTimeOfDeliveryRemark: typing.Optional[str] = None
    serviceUrl: typing.Optional[str] = None
    rerouteUrl: typing.Optional[str] = None
    details: typing.Optional[Details] = jstruct.JStruct[Details]
    events: typing.Optional[typing.List[Status]] = jstruct.JList[Status]


@attr.s(auto_attribs=True)
class TrackingResponse:
    url: typing.Optional[str] = None
    prevUrl: typing.Optional[str] = None
    nextUrl: typing.Optional[str] = None
    firstUrl: typing.Optional[str] = None
    lastUrl: typing.Optional[str] = None
    shipments: typing.Optional[typing.List[Shipment]] = jstruct.JList[Shipment]
    possibleAdditionalShipmentsUrl: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class Tracking:
    trackingRequest: typing.Optional[TrackingRequest] = jstruct.JStruct[TrackingRequest]
    trackingResponse: typing.Optional[TrackingResponse] = jstruct.JStruct[TrackingResponse]
    error: typing.Optional[Error] = jstruct.JStruct[Error]
