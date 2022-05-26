from attr import s
from typing import Optional


@s(auto_attribs=True)
class CancelShipmentResponse:
    TrackID: Optional[str] = None
    result: Optional[str] = None
