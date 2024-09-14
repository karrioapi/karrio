from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class PickupRequestType:
    courierid: Optional[str] = None
    easyshipshipmentids: List[str] = []
    selecteddate: Optional[str] = None
    selectedfromtime: Optional[str] = None
    selectedtotime: Optional[str] = None
    timeslotid: Optional[str] = None
