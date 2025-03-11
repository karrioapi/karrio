import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Location:
    city: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    stateOrRegion: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class EventHistory:
    eventCode: typing.Optional[str] = None
    location: typing.Optional[Location] = jstruct.JStruct[Location]
    eventTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Summary:
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    trackingId: typing.Optional[str] = None
    eventHistory: typing.Optional[typing.List[EventHistory]] = jstruct.JList[EventHistory]
    promisedDeliveryDate: typing.Optional[str] = None
    summary: typing.Optional[Summary] = jstruct.JStruct[Summary]
