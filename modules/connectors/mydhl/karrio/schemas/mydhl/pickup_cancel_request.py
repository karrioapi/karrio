from attr import s
from typing import Optional


@s(auto_attribs=True)
class PickupCancelRequestType:
    requestorName: Optional[str] = None
    reason: Optional[str] = None
