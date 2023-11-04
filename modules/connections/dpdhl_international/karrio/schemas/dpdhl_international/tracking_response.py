from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class EventType:
    status: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseElementType:
    events: List[EventType] = JList[EventType]
    publicUrl: Optional[str] = None
    barcode: Optional[str] = None
    awb: Optional[str] = None
