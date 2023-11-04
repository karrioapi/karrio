from attr import s
from typing import Optional


@s(auto_attribs=True)
class TrackingRequestType:
    awb: Optional[str] = None
    language: Optional[str] = None
    withEventType: Optional[bool] = None
