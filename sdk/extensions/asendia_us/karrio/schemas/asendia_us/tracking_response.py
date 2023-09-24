from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class TrackingMilestoneEventType:
    eventCode: Optional[str] = None
    eventDescription: Optional[str] = None
    eventLocation: Optional[str] = None
    eventOn: Optional[str] = None


@s(auto_attribs=True)
class DatumType:
    trackingNumberVendor: Optional[str] = None
    customerReferenceNumber: Optional[str] = None
    trackingMilestoneEvents: List[TrackingMilestoneEventType] = JList[TrackingMilestoneEventType]


@s(auto_attribs=True)
class ResponseStatusType:
    responseStatusCode: Optional[int] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    data: List[DatumType] = JList[DatumType]
    responseStatus: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
