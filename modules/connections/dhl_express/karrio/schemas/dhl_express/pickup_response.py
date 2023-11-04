from attr import s
from typing import List, Optional


@s(auto_attribs=True)
class PickupResponseType:
    dispatchConfirmationNumbers: List[str] = []
    readyByTime: Optional[str] = None
    nextPickupDate: Optional[str] = None
    warnings: List[str] = []
