import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingMilestoneEventType:
    eventCode: typing.Optional[str] = None
    eventDescription: typing.Optional[str] = None
    eventLocation: typing.Optional[str] = None
    eventOn: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DatumType:
    trackingNumberVendor: typing.Optional[str] = None
    customerReferenceNumber: typing.Optional[str] = None
    trackingMilestoneEvents: typing.Optional[typing.List[TrackingMilestoneEventType]] = jstruct.JList[TrackingMilestoneEventType]


@attr.s(auto_attribs=True)
class ResponseStatusType:
    responseStatusCode: typing.Optional[int] = None
    responseStatusMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    data: typing.Optional[typing.List[DatumType]] = jstruct.JList[DatumType]
    responseStatus: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
