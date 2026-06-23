import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingEventType:
    EventdateCET: typing.Optional[str] = None
    EventdateUTC: typing.Optional[str] = None
    Statuscode: typing.Optional[str] = None
    Status: typing.Optional[str] = None
    Location: typing.Optional[str] = None
    DeliveryStatus: typing.Optional[str] = None
    CarrierTrackno: typing.Optional[str] = None
    Carrier: typing.Optional[str] = None
    CarrierSlug: typing.Optional[str] = None
    CarrierTrackURL: typing.Optional[str] = None
    TrackingEventsStatus: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    P1Trackno: typing.Optional[str] = None
    TrackingEvents: typing.Optional[typing.List[TrackingEventType]] = jstruct.JList[TrackingEventType]
    lang: typing.Optional[str] = None
    platform: typing.Optional[str] = None
    requestor: typing.Optional[str] = None
