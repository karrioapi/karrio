from attr import s
from typing import Optional


@s(auto_attribs=True)
class RateResponseElementType:
    deliverySpeed: Optional[str] = None
    price: Optional[int] = None
    deliveredBy: Optional[str] = None
    earliestPickupEta: Optional[str] = None
    earliestDropEta: Optional[str] = None
