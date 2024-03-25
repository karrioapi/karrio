from attr import s
from typing import Optional


@s(auto_attribs=True)
class TrackingRequestType:
    ref: Optional[int] = None
