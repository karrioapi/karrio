from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ErrorType:
    title: Optional[str] = None
    detail: Optional[str] = None
    status: Optional[int] = None
    instance: Optional[str] = None


@s(auto_attribs=True)
class TrackingRequestType:
    trackingNumber: Optional[str] = None
    service: Optional[str] = None
    requesterCountryCode: Optional[str] = None
    originCountryCode: Optional[str] = None
    recipientPostalCode: Optional[str] = None
    language: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


@s(auto_attribs=True)
class AddressType:
    countryCode: Optional[str] = None
    postalCode: Optional[str] = None
    addressLocality: Optional[str] = None


@s(auto_attribs=True)
class DestinationType:
    address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class CarrierType:
    type: Optional[str] = None
    organizationName: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    value: Optional[float] = None
    unitText: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    width: Optional[WeightType] = JStruct[WeightType]
    height: Optional[WeightType] = JStruct[WeightType]
    length: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class ProductType:
    productName: Optional[str] = None


@s(auto_attribs=True)
class ReceiverType:
    type: Optional[str] = None
    familyName: Optional[str] = None
    givenName: Optional[str] = None
    name: Optional[str] = None
    organizationName: Optional[str] = None


@s(auto_attribs=True)
class ProofOfDeliveryType:
    timestamp: Optional[str] = None
    signatureUrl: Optional[str] = None
    documentUrl: Optional[str] = None
    signed: Optional[ReceiverType] = JStruct[ReceiverType]


@s(auto_attribs=True)
class ReferencesType:
    number: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class VolumeType:
    value: Optional[int] = None


@s(auto_attribs=True)
class DetailsType:
    carrier: Optional[CarrierType] = JStruct[CarrierType]
    product: Optional[ProductType] = JStruct[ProductType]
    receiver: Optional[ReceiverType] = JStruct[ReceiverType]
    sender: Optional[ReceiverType] = JStruct[ReceiverType]
    proofOfDelivery: Optional[ProofOfDeliveryType] = JStruct[ProofOfDeliveryType]
    totalNumberOfPieces: Optional[int] = None
    pieceIds: List[str] = []
    weight: Optional[WeightType] = JStruct[WeightType]
    volume: Optional[VolumeType] = JStruct[VolumeType]
    loadingMeters: Optional[float] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    references: Optional[ReferencesType] = JStruct[ReferencesType]


@s(auto_attribs=True)
class EstimatedDeliveryTimeFrameType:
    estimatedFrom: Optional[str] = None
    estimatedThrough: Optional[str] = None


@s(auto_attribs=True)
class StatusType:
    timestamp: Optional[str] = None
    location: Optional[DestinationType] = JStruct[DestinationType]
    statusCode: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    remark: Optional[str] = None
    nextSteps: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    id: Optional[int] = None
    service: Optional[str] = None
    origin: Optional[DestinationType] = JStruct[DestinationType]
    destination: Optional[DestinationType] = JStruct[DestinationType]
    status: Optional[StatusType] = JStruct[StatusType]
    estimatedTimeOfDelivery: Optional[str] = None
    estimatedDeliveryTimeFrame: Optional[EstimatedDeliveryTimeFrameType] = JStruct[EstimatedDeliveryTimeFrameType]
    estimatedTimeOfDeliveryRemark: Optional[str] = None
    serviceUrl: Optional[str] = None
    rerouteUrl: Optional[str] = None
    details: Optional[DetailsType] = JStruct[DetailsType]
    events: List[StatusType] = JList[StatusType]


@s(auto_attribs=True)
class TrackingResponseClassType:
    url: Optional[str] = None
    prevUrl: Optional[str] = None
    nextUrl: Optional[str] = None
    firstUrl: Optional[str] = None
    lastUrl: Optional[str] = None
    shipments: List[ShipmentType] = JList[ShipmentType]
    possibleAdditionalShipmentsUrl: List[str] = []


@s(auto_attribs=True)
class TrackingResponseType:
    trackingRequest: Optional[TrackingRequestType] = JStruct[TrackingRequestType]
    trackingResponse: Optional[TrackingResponseClassType] = JStruct[TrackingResponseClassType]
    error: Optional[ErrorType] = JStruct[ErrorType]
