from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Error:
    title: Optional[str] = None
    detail: Optional[str] = None
    status: Optional[int] = None
    instance: Optional[str] = None


@s(auto_attribs=True)
class TrackingRequest:
    trackingNumber: Optional[str] = None
    service: Optional[str] = None
    requesterCountryCode: Optional[str] = None
    originCountryCode: Optional[str] = None
    recipientPostalCode: Optional[str] = None
    language: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


@s(auto_attribs=True)
class Address:
    countryCode: Optional[str] = None
    postalCode: Optional[str] = None
    addressLocality: Optional[str] = None


@s(auto_attribs=True)
class Destination:
    address: Optional[Address] = JStruct[Address]


@s(auto_attribs=True)
class Carrier:
    type: Optional[str] = None
    organizationName: Optional[str] = None


@s(auto_attribs=True)
class Weight:
    value: Optional[float] = None
    unitText: Optional[str] = None


@s(auto_attribs=True)
class Dimensions:
    width: Optional[Weight] = JStruct[Weight]
    height: Optional[Weight] = JStruct[Weight]
    length: Optional[Weight] = JStruct[Weight]


@s(auto_attribs=True)
class Product:
    productName: Optional[str] = None


@s(auto_attribs=True)
class Receiver:
    type: Optional[str] = None
    familyName: Optional[str] = None
    givenName: Optional[str] = None
    name: Optional[str] = None
    organizationName: Optional[str] = None


@s(auto_attribs=True)
class ProofOfDelivery:
    timestamp: Optional[str] = None
    signatureUrl: Optional[str] = None
    documentUrl: Optional[str] = None
    signed: Optional[Receiver] = JStruct[Receiver]


@s(auto_attribs=True)
class References:
    number: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class Volume:
    value: Optional[int] = None


@s(auto_attribs=True)
class Details:
    carrier: Optional[Carrier] = JStruct[Carrier]
    product: Optional[Product] = JStruct[Product]
    receiver: Optional[Receiver] = JStruct[Receiver]
    sender: Optional[Receiver] = JStruct[Receiver]
    proofOfDelivery: Optional[ProofOfDelivery] = JStruct[ProofOfDelivery]
    totalNumberOfPieces: Optional[int] = None
    pieceIds: List[str] = []
    weight: Optional[Weight] = JStruct[Weight]
    volume: Optional[Volume] = JStruct[Volume]
    loadingMeters: Optional[float] = None
    dimensions: Optional[Dimensions] = JStruct[Dimensions]
    references: Optional[References] = JStruct[References]


@s(auto_attribs=True)
class EstimatedDeliveryTimeFrame:
    estimatedFrom: Optional[str] = None
    estimatedThrough: Optional[str] = None


@s(auto_attribs=True)
class Status:
    timestamp: Optional[str] = None
    location: Optional[Destination] = JStruct[Destination]
    statusCode: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    remark: Optional[str] = None
    nextSteps: Optional[str] = None


@s(auto_attribs=True)
class Shipment:
    id: Optional[int] = None
    service: Optional[str] = None
    origin: Optional[Destination] = JStruct[Destination]
    destination: Optional[Destination] = JStruct[Destination]
    status: Optional[Status] = JStruct[Status]
    estimatedTimeOfDelivery: Optional[str] = None
    estimatedDeliveryTimeFrame: Optional[EstimatedDeliveryTimeFrame] = JStruct[EstimatedDeliveryTimeFrame]
    estimatedTimeOfDeliveryRemark: Optional[str] = None
    serviceUrl: Optional[str] = None
    rerouteUrl: Optional[str] = None
    details: Optional[Details] = JStruct[Details]
    events: List[Status] = JList[Status]


@s(auto_attribs=True)
class TrackingResponse:
    url: Optional[str] = None
    prevUrl: Optional[str] = None
    nextUrl: Optional[str] = None
    firstUrl: Optional[str] = None
    lastUrl: Optional[str] = None
    shipments: List[Shipment] = JList[Shipment]
    possibleAdditionalShipmentsUrl: List[str] = []


@s(auto_attribs=True)
class Tracking:
    trackingRequest: Optional[TrackingRequest] = JStruct[TrackingRequest]
    trackingResponse: Optional[TrackingResponse] = JStruct[TrackingResponse]
    error: Optional[Error] = JStruct[Error]
