from attr import s
from typing import Optional, Any, List
from jstruct import JList


@s(auto_attribs=True)
class EventType:
    EventDT: Optional[str] = None
    Code: Any = None
    OmniCode: Optional[str] = None
    Description: Optional[str] = None
    Location: Optional[str] = None
    Part: Optional[int] = None


@s(auto_attribs=True)
class TrackingResponseElementType:
    ConsignmentNo: Optional[str] = None
    Status: Optional[str] = None
    Picked: Any = None
    Delivered: Any = None
    Tracking: Optional[str] = None
    Reference1: Optional[str] = None
    Events: List[EventType] = JList[EventType]
