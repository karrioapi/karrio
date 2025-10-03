import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DestinationType:
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SchedulingType:
    pickup_date: typing.Optional[str] = None
    picked_up_on: typing.Optional[str] = None
    delivered_on: typing.Optional[str] = None
    estimated_delivery_date_minimum: typing.Optional[str] = None
    estimated_delivery_date_maximum: typing.Optional[str] = None
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatusType:
    description: typing.Optional[str] = None
    last_changed_at: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingEventType:
    event_type: typing.Optional[str] = None
    scan_time: typing.Optional[str] = None
    description: typing.Optional[str] = None
    reason: typing.Optional[str] = None
    display_time: typing.Optional[str] = None
    origin_location: typing.Optional[str] = None
    destination_location: typing.Optional[str] = None
    location: typing.Optional[str] = None
    requester: typing.Optional[str] = None
    local_scan_time: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    state: typing.Optional[str] = None
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    origin: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    scheduling: typing.Optional[SchedulingType] = jstruct.JStruct[SchedulingType]
    tracking_events: typing.Optional[typing.List[TrackingEventType]] = jstruct.JList[TrackingEventType]
