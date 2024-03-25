from attr import s
from typing import Optional


@s(auto_attribs=True)
class VoidRequestType:
    shipmentno: Optional[int] = None
    postalcode: Optional[int] = None
