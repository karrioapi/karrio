"""Sendle Tracking Datatypes definition module."""

import attr
from typing import List
from jstruct import JList


@attr.s(auto_attribs=True)
class Event:
    event_type: str = None
    scan_time: str = None
    description: str = None
    origin_location: str = None
    destination_location: str = None
    reason: str = None
    requester: str = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    state: str = None
    tracking_events: List[Event] = JList[Event]
