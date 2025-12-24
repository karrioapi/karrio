import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LocationType:
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EventType:
    timestamp: typing.Optional[str] = None
    status: typing.Optional[str] = None
    description: typing.Optional[str] = None
    location: typing.Optional[LocationType] = jstruct.JStruct[LocationType]


@attr.s(auto_attribs=True)
class ReceiverType:
    name: typing.Optional[str] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    trackingNumber: typing.Optional[str] = None
    status: typing.Optional[str] = None
    shipmentId: typing.Optional[str] = None
    product: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    sender: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    receiver: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    estimatedDelivery: typing.Optional[str] = None
