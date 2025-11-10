import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EventType:
    timestamp: typing.Optional[str] = None
    status: typing.Optional[str] = None
    location: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StMileType:
    status: typing.Optional[str] = None
    carrier: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipType:
    name: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postcode: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    status: typing.Optional[str] = None
    shipmentId: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    customerReference: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    estimatedDelivery: typing.Optional[str] = None
    shipFrom: typing.Optional[ShipType] = jstruct.JStruct[ShipType]
    shipTo: typing.Optional[ShipType] = jstruct.JStruct[ShipType]
    firstMile: typing.Optional[StMileType] = jstruct.JStruct[StMileType]
    lastMile: typing.Optional[StMileType] = jstruct.JStruct[StMileType]
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
