from attr import s
from typing import Optional


@s(auto_attribs=True)
class CancelShipmentRequestType:
    countryCode: Optional[str] = None
    trackingNo: Optional[str] = None
