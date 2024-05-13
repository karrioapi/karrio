from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class OrderType:
    trackingId: Optional[str] = None
    orderId: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class CancelRequestType:
    order: Optional[OrderType] = JStruct[OrderType]
