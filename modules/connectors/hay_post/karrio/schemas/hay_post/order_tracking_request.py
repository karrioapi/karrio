from attr import s
from typing import Optional


@s(auto_attribs=True)
class OrderTrackingRequestType:
    trackingnumber: Optional[int] = None
