import attr
from jstruct import JStruct, JList
from typing import Optional, List


@attr.s(auto_attribs=True)
class Location:
    country: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingEvent:
    eventtype: Optional[str] = None
    scantime: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[str] = None
    originlocation: Optional[str] = None
    destinationlocation: Optional[str] = None
    locaion: Optional[str] = None
    requester: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    state: Optional[str] = None
    trackingevents: Optional[List[TrackingEvent]] = JList[TrackingEvent]
    origin: Optional[Location] = JStruct[Location]
    destination: Optional[Location] = JStruct[Location]
