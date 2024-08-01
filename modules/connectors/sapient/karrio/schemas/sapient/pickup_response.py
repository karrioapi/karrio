from attr import s
from typing import Optional


@s(auto_attribs=True)
class PickupResponseType:
    CollectionOrderId: Optional[str] = None
    CollectionDate: Optional[str] = None
