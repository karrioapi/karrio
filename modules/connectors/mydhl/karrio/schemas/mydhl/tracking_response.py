import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressType:
    addressLocality: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    addressCountry: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServicePointType:
    url: typing.Optional[str] = None
    label: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DestinationType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    servicePoint: typing.Optional[ServicePointType] = jstruct.JStruct[ServicePointType]


@attr.s(auto_attribs=True)
class ServiceAreaType:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EventType:
    date: typing.Optional[str] = None
    time: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    serviceArea: typing.Optional[typing.List[ServiceAreaType]] = jstruct.JList[ServiceAreaType]


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PieceType:
    number: typing.Optional[int] = None
    typeCode: typing.Optional[str] = None
    shipmentTrackingNumber: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    description: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensionalWeight: typing.Optional[float] = None
    actualWeight: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    actualDimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]


@attr.s(auto_attribs=True)
class ShipmentType:
    shipmentTrackingNumber: typing.Optional[int] = None
    status: typing.Optional[str] = None
    shipmentTimestamp: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    estimatedTimeOfDelivery: typing.Optional[str] = None
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    pieces: typing.Optional[typing.List[PieceType]] = jstruct.JList[PieceType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    shipments: typing.Optional[typing.List[ShipmentType]] = jstruct.JList[ShipmentType]
