from attr import s
from typing import Optional


@s(auto_attribs=True)
class ShippingResponseType:
    reference: Optional[str] = None
    price: Optional[float] = None
    trackinglink: Optional[str] = None
    trackingCode: Optional[str] = None
