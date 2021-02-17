import attr
from typing import Optional, List
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class Event:
    eventCode: Optional[str] = None
    eventName: Optional[str] = None
    eventDateTime: Optional[str] = None
    locationName: Optional[str] = None


@attr.s(auto_attribs=True)
class MailPieces:
    mailPieceId: Optional[str] = None
    carrierShortName: Optional[str] = None
    carrierFullName: Optional[str] = None
    summary: Optional[dict] = None
    signature: Optional[dict] = None
    estimatedDelivery: Optional[dict] = None
    events: Optional[List[Event]] = JList[Event]
    links: Optional[dict] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    mailPieces: Optional[MailPieces] = None
