from attr import s
from typing import Optional


@s(auto_attribs=True)
class TrackingRequest:
    noSuivi: Optional[str] = None
