import attr
from jstruct import JList, JStruct
from typing import Optional, List


@dataclass
class Checkpoint:
    time_stamp: Optional[str] = None
    time_zone: Optional[str] = None
    tracking_status: Optional[str] = None
    message: Optional[str] = None
    location: Optional[str] = None


@dataclass
class Result:
    tracking_number: Optional[str] = None
    tracking_status: Optional[str] = None
    last_mile_tracking_expected: Optional[bool] = None
    checkpoints: Optional[List[Checkpoint]] = JList[Checkpoint]


@dataclass
class TrackingResponse:
    code: Optional[int] = None
    message: Optional[str] = None
    result: Optional[List[Result]] = JList[Result]
    elapsedMilliseconds: Optional[int] = None
