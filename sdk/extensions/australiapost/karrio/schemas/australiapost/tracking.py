"""Australia Post Tracking Datatype definition module."""

import attr
from typing import Optional, List
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class TrackingRequest:
    tracking_ids: Optional[str] = None


@attr.s(auto_attribs=True)
class Event:
    location: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None


@attr.s(auto_attribs=True)
class Consignment:
    events: Optional[List[Event]] = JList[Event]
    status: Optional[str] = None


@attr.s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    name: Optional[str] = None
    message: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackableItem:
    article_id: Optional[str] = None
    product_type: Optional[str] = None
    events: Optional[List[Event]] = JList[Event]
    status: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResult:
    tracking_id: Optional[str] = None
    errors: Optional[List[Error]] = JList[Error]
    status: Optional[str] = None
    trackable_items: Optional[List[TrackableItem]] = JList[TrackableItem]
    consignment: Optional[List[Consignment]] = JList[Consignment]


@attr.s(auto_attribs=True)
class TrackingResponse:
    tracking_results: Optional[List[TrackingResult]] = JList[TrackingResult]
    errors:  Optional[List[Error]] = JList[Error]
