from attr import s
from typing import Optional


@s(auto_attribs=True)
class TrackingRequestType:
    noSuivi: Optional[str] = None
    refUniExp: Optional[str] = None
