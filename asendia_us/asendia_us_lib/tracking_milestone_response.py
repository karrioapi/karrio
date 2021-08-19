from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class TrackingMilestoneEvent:
    eventCode: Optional[str] = None
    eventDescription: Optional[str] = None
    eventLocation: Optional[str] = None
    eventOn: Optional[str] = None


@s(auto_attribs=True)
class Datum:
    trackingNumberVendor: Optional[str] = None
    customerReferenceNumber: Optional[str] = None
    trackingMilestoneEvents: List[TrackingMilestoneEvent] = JList[TrackingMilestoneEvent]


@s(auto_attribs=True)
class ResponseStatus:
    responseStatusCode: Optional[int] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class TrackingMilestoneResponse:
    data: List[Datum] = JList[Datum]
    responseStatus: Optional[ResponseStatus] = JStruct[ResponseStatus]
