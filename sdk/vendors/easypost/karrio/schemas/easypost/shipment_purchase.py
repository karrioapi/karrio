from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class Rate:
    id: Optional[str] = None


@s(auto_attribs=True)
class ShipmentPurchase:
    insurance: Optional[float] = None
    rate: Optional[Rate] = JStruct[Rate]
