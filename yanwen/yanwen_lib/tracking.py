import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Checkpoint:
    time_stamp: Optional[str] = None
    time_zone: Optional[str] = None
    tracking_status: Optional[str] = None
    message: Optional[str] = None
    location: Optional[str] = None


@attr.s(auto_attribs=True)
class Result:
    tracking_number: Optional[str] = None
    tracking_status: Optional[str] = None
    last_mile_tracking_expected: Optional[bool] = None
    checkpoints: Optional[List[Checkpoint]] = JList[Checkpoint]


@attr.s(auto_attribs=True)
class TrackingResponse:
    code: Optional[int] = None
    message: Optional[str] = None
    result: Optional[List[Result]] = JList[Result]
    elapsedMilliseconds: Optional[int] = None
