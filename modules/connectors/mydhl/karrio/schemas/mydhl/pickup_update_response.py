from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class PickupUpdateResponseType:
    dispatchConfirmationNumber: Optional[str] = None
    readyByTime: Optional[str] = None
    nextPickupDate: Optional[str] = None
    warnings: List[str] = []
