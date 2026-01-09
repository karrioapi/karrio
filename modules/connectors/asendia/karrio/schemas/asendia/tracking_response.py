import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingEventType:
    id: typing.Optional[int] = None
    code: typing.Optional[str] = None
    time: typing.Optional[str] = None
    locationName: typing.Optional[str] = None
    carrierEventDescription: typing.Optional[str] = None
    locationCountry: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    trackingNumber: typing.Optional[str] = None
    trackingEvents: typing.Optional[typing.List[TrackingEventType]] = jstruct.JList[TrackingEventType]
