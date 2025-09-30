import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EventType:
    EventDT: typing.Optional[str] = None
    Code: typing.Any = None
    OmniCode: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    Location: typing.Optional[str] = None
    Part: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class TrackingResponseElementType:
    ConsignmentNo: typing.Optional[str] = None
    Status: typing.Optional[str] = None
    Picked: typing.Any = None
    Delivered: typing.Any = None
    Tracking: typing.Optional[str] = None
    Reference1: typing.Optional[str] = None
    Events: typing.Optional[typing.List[EventType]] = jstruct.JList[EventType]
