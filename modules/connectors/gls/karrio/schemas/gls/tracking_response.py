import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EventType:
    code: typing.Optional[str] = None
    city: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    country: typing.Optional[str] = None
    description: typing.Optional[str] = None
    eventDateTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    requested: typing.Optional[str] = None
    unitno: typing.Optional[str] = None
    status: typing.Optional[str] = None
    statusDateTime: typing.Optional[str] = None
    events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
    errorCode: typing.Any = None
    errorMessage: typing.Any = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
