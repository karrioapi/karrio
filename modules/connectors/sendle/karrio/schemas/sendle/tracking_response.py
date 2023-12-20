from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DestinationType:
    country: Optional[str] = None


@s(auto_attribs=True)
class SchedulingType:
    pickup_date: Optional[str] = None
    picked_up_on: Optional[str] = None
    delivered_on: Optional[str] = None
    estimated_delivery_date_minimum: Optional[str] = None
    estimated_delivery_date_maximum: Optional[str] = None
    status: Optional[str] = None


@s(auto_attribs=True)
class StatusType:
    description: Optional[str] = None
    last_changed_at: Optional[str] = None


@s(auto_attribs=True)
class TrackingEventType:
    event_type: Optional[str] = None
    scan_time: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[str] = None
    display_time: Optional[str] = None
    location: Optional[str] = None
    local_scan_time: Optional[str] = None
    origin_location: Optional[str] = None
    destination_location: Optional[str] = None
    location: Optional[str] = None
    requester: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    state: Optional[str] = None
    status: Optional[StatusType] = JStruct[StatusType]
    origin: Optional[DestinationType] = JStruct[DestinationType]
    destination: Optional[DestinationType] = JStruct[DestinationType]
    scheduling: Optional[SchedulingType] = JStruct[SchedulingType]
    tracking_events: List[TrackingEventType] = JList[TrackingEventType]
