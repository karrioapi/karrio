import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EventType:
    timestamp: typing.Optional[str] = None
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    location: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StMileType:
    carrier: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    trackingUrl: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    line1: typing.Optional[str] = None
    line2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    postcode: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipType:
    name: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]


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
