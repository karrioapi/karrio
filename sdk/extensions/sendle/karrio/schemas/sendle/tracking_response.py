from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Destination:
    country: Optional[str] = None


@s(auto_attribs=True)
class Scheduling:
    pickup_date: Optional[str] = None
    picked_up_on: Optional[str] = None
    delivered_on: Optional[str] = None
    estimated_delivery_date_minimum: Optional[str] = None
    estimated_delivery_date_maximum: Optional[str] = None


@s(auto_attribs=True)
class Status:
    description: Optional[str] = None
    last_changed_at: Optional[str] = None


@s(auto_attribs=True)
class TrackingEvent:
    event_type: Optional[str] = None
    scan_time: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[str] = None
    local_scan_time: Optional[str] = None
    location: Optional[str] = None
    origin_location: Optional[str] = None
    destination_location: Optional[str] = None
    requester: Optional[str] = None


@s(auto_attribs=True)
class Tracking:
    state: Optional[str] = None
    status: Optional[Status] = JStruct[Status]
    tracking_events: List[TrackingEvent] = JList[TrackingEvent]
    origin: Optional[Destination] = JStruct[Destination]
    destination: Optional[Destination] = JStruct[Destination]
    scheduling: Optional[Scheduling] = JStruct[Scheduling]


@s(auto_attribs=True)
class TrackingResponse:
    tracking: List[Tracking] = JList[Tracking]
