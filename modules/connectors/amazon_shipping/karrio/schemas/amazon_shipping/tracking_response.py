from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Location:
    city: Optional[str] = None
    countryCode: Optional[str] = None
    stateOrRegion: Optional[str] = None
    postalCode: Optional[int] = None


@s(auto_attribs=True)
class EventHistory:
    eventCode: Optional[str] = None
    location: Optional[Location] = JStruct[Location]
    eventTime: Optional[str] = None


@s(auto_attribs=True)
class Summary:
    status: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponse:
    trackingId: Optional[str] = None
    eventHistory: List[EventHistory] = JList[EventHistory]
    promisedDeliveryDate: Optional[str] = None
    summary: Optional[Summary] = JStruct[Summary]
