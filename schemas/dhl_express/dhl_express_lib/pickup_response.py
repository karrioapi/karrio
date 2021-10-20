from attr import s
from typing import List, Optional
from jstruct import JList


@s(auto_attribs=True)
class PickupResponse:
    dispatchConfirmationNumbers: List[str] = JList[str]
    readyByTime: Optional[str] = None
    nextPickupDate: Optional[str] = None
    warnings: List[str] = JList[str]
