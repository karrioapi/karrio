import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EventServiceAreaType:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EventType:
    date: typing.Optional[str] = None
    time: typing.Optional[str] = None
    GMTOffset: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    serviceArea: typing.Optional[typing.List[EventServiceAreaType]] = jstruct.JList[EventServiceAreaType]
    signedBy: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PieceType:
    number: typing.Optional[int] = None
    typeCode: typing.Optional[str] = None
    shipmentTrackingNumber: typing.Optional[int] = None
    trackingNumber: typing.Optional[str] = None
    description: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensionalWeight: typing.Optional[float] = None
    actualWeight: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    actualDimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    shippedQuantity: typing.Optional[int] = None
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]


@attr.s(auto_attribs=True)
class PostalAddressType:
    cityName: typing.Optional[str] = None
    countyName: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    provinceCode: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverDetailsServiceAreaType:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    facilityCode: typing.Optional[str] = None
    inboundSortCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverDetailsType:
    name: typing.Optional[str] = None
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    serviceArea: typing.Optional[typing.List[ReceiverDetailsServiceAreaType]] = jstruct.JList[ReceiverDetailsServiceAreaType]


@attr.s(auto_attribs=True)
class ShipperDetailsServiceAreaType:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    outboundSortCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipperDetailsType:
    name: typing.Optional[str] = None
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    serviceArea: typing.Optional[typing.List[ShipperDetailsServiceAreaType]] = jstruct.JList[ShipperDetailsServiceAreaType]


@attr.s(auto_attribs=True)
class ShipperReferenceType:
    value: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    shipmentTrackingNumber: typing.Optional[int] = None
    status: typing.Optional[str] = None
    shipmentTimestamp: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    shipperDetails: typing.Optional[ShipperDetailsType] = jstruct.JStruct[ShipperDetailsType]
    receiverDetails: typing.Optional[ReceiverDetailsType] = jstruct.JStruct[ReceiverDetailsType]
    totalWeight: typing.Optional[float] = None
    unitOfMeasurements: typing.Optional[str] = None
    shipperReferences: typing.Optional[typing.List[ShipperReferenceType]] = jstruct.JList[ShipperReferenceType]
    estimatedTimeOfDelivery: typing.Optional[str] = None
    estimatedTimeOfDeliveryRemark: typing.Optional[str] = None
    numberOfPieces: typing.Optional[int] = None
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    pieces: typing.Optional[typing.List[PieceType]] = jstruct.JList[PieceType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
