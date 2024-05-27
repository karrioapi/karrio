from attr import s
from typing import Optional


@s(auto_attribs=True)
class PickupCancelResponseType:
    orderId: Optional[int] = None
    status: Optional[str] = None
