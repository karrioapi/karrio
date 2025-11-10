import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LocationType:
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class EventType:
    timestamp: typing.Optional[str] = None
    status: typing.Optional[str] = None
    description: typing.Optional[str] = None
    location: typing.Optional[LocationType] = jstruct.JStruct[LocationType]
    signedBy: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RecipientType:
    name: typing.Optional[str] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    trackingNumber: typing.Optional[str] = None
    shipmentId: typing.Optional[str] = None
    status: typing.Optional[str] = None
    statusDescription: typing.Optional[str] = None
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    estimatedDelivery: typing.Optional[str] = None
    recipient: typing.Optional[RecipientType] = jstruct.JStruct[RecipientType]
