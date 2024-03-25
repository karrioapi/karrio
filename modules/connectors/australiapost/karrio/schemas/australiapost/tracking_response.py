from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class EventType:
    location: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None


@s(auto_attribs=True)
class ConsignmentType:
    events: List[EventType] = JList[EventType]
    status: Optional[str] = None


@s(auto_attribs=True)
class ErrorType:
    code: Optional[str] = None
    name: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    article_id: Optional[str] = None
    product_type: Optional[str] = None
    events: List[EventType] = JList[EventType]
    status: Optional[str] = None


@s(auto_attribs=True)
class TrackableItemType:
    article_id: Optional[str] = None
    product_type: Optional[str] = None
    events: List[EventType] = JList[EventType]
    status: Optional[str] = None
    consignment_id: Optional[str] = None
    number_of_items: Optional[int] = None
    items: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class TrackingResultType:
    tracking_id: Optional[str] = None
    errors: List[ErrorType] = JList[ErrorType]
    status: Optional[str] = None
    trackable_items: List[TrackableItemType] = JList[TrackableItemType]
    consignment: List[ConsignmentType] = JList[ConsignmentType]


@s(auto_attribs=True)
class TrackingResponseType:
    tracking_results: List[TrackingResultType] = JList[TrackingResultType]
