from attr import s
from typing import Optional


@s(auto_attribs=True)
class CancelShipmentResponseType:
    trackingId: Optional[str] = None
    status: Optional[str] = None
    updatedAt: Optional[str] = None
