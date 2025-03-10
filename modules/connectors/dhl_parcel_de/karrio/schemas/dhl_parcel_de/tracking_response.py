import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    title: typing.Optional[str] = None
    detail: typing.Optional[str] = None
    status: typing.Optional[int] = None
    instance: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingRequestType:
    trackingNumber: typing.Optional[str] = None
    service: typing.Optional[str] = None
    requesterCountryCode: typing.Optional[str] = None
    originCountryCode: typing.Optional[str] = None
    recipientPostalCode: typing.Optional[str] = None
    language: typing.Optional[str] = None
    offset: typing.Optional[int] = None
    limit: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class AddressType:
    countryCode: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    addressLocality: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DestinationType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


@attr.s(auto_attribs=True)
class CarrierType:
    type: typing.Optional[str] = None
    organizationName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    value: typing.Optional[float] = None
    unitText: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    width: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    height: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    length: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class ProductType:
    productName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverType:
    type: typing.Optional[str] = None
    familyName: typing.Optional[str] = None
    givenName: typing.Optional[str] = None
    name: typing.Optional[str] = None
    organizationName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ProofOfDeliveryType:
    timestamp: typing.Optional[str] = None
    signatureUrl: typing.Optional[str] = None
    documentUrl: typing.Optional[str] = None
    signed: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]


@attr.s(auto_attribs=True)
class ReferencesType:
    number: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class VolumeType:
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DetailsType:
    carrier: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    product: typing.Optional[ProductType] = jstruct.JStruct[ProductType]
    receiver: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    sender: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    proofOfDelivery: typing.Optional[ProofOfDeliveryType] = jstruct.JStruct[ProofOfDeliveryType]
    totalNumberOfPieces: typing.Optional[int] = None
    pieceIds: typing.Optional[typing.List[str]] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    volume: typing.Optional[VolumeType] = jstruct.JStruct[VolumeType]
    loadingMeters: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    references: typing.Optional[ReferencesType] = jstruct.JStruct[ReferencesType]


@attr.s(auto_attribs=True)
class EstimatedDeliveryTimeFrameType:
    estimatedFrom: typing.Optional[str] = None
    estimatedThrough: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatusType:
    timestamp: typing.Optional[str] = None
    location: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    statusCode: typing.Optional[str] = None
    status: typing.Optional[str] = None
    description: typing.Optional[str] = None
    remark: typing.Optional[str] = None
    nextSteps: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    id: typing.Optional[int] = None
    service: typing.Optional[str] = None
    origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    estimatedTimeOfDelivery: typing.Optional[str] = None
    estimatedDeliveryTimeFrame: typing.Optional[EstimatedDeliveryTimeFrameType] = jstruct.JStruct[EstimatedDeliveryTimeFrameType]
    estimatedTimeOfDeliveryRemark: typing.Optional[str] = None
    serviceUrl: typing.Optional[str] = None
    rerouteUrl: typing.Optional[str] = None
    details: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    events: typing.Optional[typing.List[StatusType]] = jstruct.JList[StatusType]


@attr.s(auto_attribs=True)
class TrackingResponseClassType:
    url: typing.Optional[str] = None
    prevUrl: typing.Optional[str] = None
    nextUrl: typing.Optional[str] = None
    firstUrl: typing.Optional[str] = None
    lastUrl: typing.Optional[str] = None
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
    possibleAdditionalShipmentsUrl: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    trackingRequest: typing.Optional[TrackingRequestType] = jstruct.JStruct[TrackingRequestType]
    trackingResponse: typing.Optional[TrackingResponseClassType] = jstruct.JStruct[TrackingResponseClassType]
    error: typing.Optional[ErrorType] = jstruct.JStruct[ErrorType]
