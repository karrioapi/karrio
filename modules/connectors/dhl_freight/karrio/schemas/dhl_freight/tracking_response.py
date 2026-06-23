import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressType:
    countryCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
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
    value: typing.Optional[int] = None
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
class ReferencesType:
    number: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class VolumeType:
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class DetailsType:
    carrier: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    product: typing.Optional[ProductType] = jstruct.JStruct[ProductType]
    receiver: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    sender: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    totalNumberOfPieces: typing.Optional[int] = None
    pieceIds: typing.Optional[typing.List[str]] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    volume: typing.Optional[VolumeType] = jstruct.JStruct[VolumeType]
    loadingMeters: typing.Optional[int] = None
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
    id: typing.Optional[str] = None
    service: typing.Optional[str] = None
    origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    estimatedTimeOfDelivery: typing.Optional[str] = None
    estimatedDeliveryTimeFrame: typing.Optional[EstimatedDeliveryTimeFrameType] = jstruct.JStruct[EstimatedDeliveryTimeFrameType]
    serviceUrl: typing.Optional[str] = None
    details: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    events: typing.Optional[typing.List[StatusType]] = jstruct.JList[StatusType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    url: typing.Optional[str] = None
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
