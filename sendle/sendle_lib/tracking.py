import attr
from jstruct import JStruct, JList
from typing import Optional, List


@attr.s(auto_attribs=True)
class Location:
    country: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingEvent:
    event_type: Optional[str] = None
    scan_time: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[str] = None
    origin_location: Optional[str] = None
    destination_location: Optional[str] = None
    location: Optional[str] = None
    requester: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingDetails:
    state: Optional[str] = None
    tracking_events: Optional[List[TrackingEvent]] = None
    origin: Optional[Location] = JStruct[Location]
    destination: Optional[Location] = JStruct[Location]


@attr.s(auto_attribs=True)
class TrackingResponse:
    tracking_number: Optional[str] = None
    tracking_details: Optional[TrackingDetails] = None
