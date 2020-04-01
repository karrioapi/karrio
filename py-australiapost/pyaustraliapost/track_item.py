"""Australia Post Tracking Datatype definition module."""

import attr
from typing import List
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class Event:
    location: str = None
    description: str = None
    date: str = None


@attr.s(auto_attribs=True)
class Consignment:
    events: List[Event] = JList[Event]
    status: str = None


@attr.s(auto_attribs=True)
class TrackingError:
    code: str = None
    name: str = None


@attr.s(auto_attribs=True)
class TrackableItem:
    article_id: str = None
    product_type: str = None
    status: str = None
    events: List[Event] = JList[Event]


@attr.s(auto_attribs=True)
class TrackingResult:
    status: str = None
    tracking_id: str = None
    consignment: Consignment = JStruct[Consignment]
    errors: List[TrackingError] = JList[TrackingError]
    trackable_items: List[TrackableItem] = JList[TrackableItem]


@attr.s(auto_attribs=True)
class Error:
    code: str = None
    name: str = None
    message: str = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    tracking_results: List[TrackingResult] = JList[TrackingResult]
    errors: List[Error] = JList[Error]
