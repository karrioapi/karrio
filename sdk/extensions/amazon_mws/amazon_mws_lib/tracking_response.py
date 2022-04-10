from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None


@s(auto_attribs=True)
class Location:
    stateOrRegion: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = None
    postalCode: Optional[str] = None


@s(auto_attribs=True)
class EventHistory:
    eventCode: Optional[str] = None
    eventTime: Optional[str] = None
    location: Optional[Location] = JStruct[Location]


@s(auto_attribs=True)
class Summary:
    status: Optional[str] = None


@s(auto_attribs=True)
class Payload:
    trackingId: Optional[str] = None
    summary: Optional[Summary] = JStruct[Summary]
    promisedDeliveryDate: Optional[str] = None
    eventHistory: List[EventHistory] = JList[EventHistory]


@s(auto_attribs=True)
class TrackingResponse:
    payload: Optional[Payload] = JStruct[Payload]
    errors: List[Error] = JList[Error]
