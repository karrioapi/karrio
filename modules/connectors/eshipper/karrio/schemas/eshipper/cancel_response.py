from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class OrderType:
    trackingId: Optional[str] = None
    orderId: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class CancelResponseType:
    order: List[OrderType] = JList[OrderType]
