from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Rate:
    id: Optional[str] = None


@s(auto_attribs=True)
class Shipment:
    insurance: Optional[float] = None
    rate: Optional[Rate] = JStruct[Rate]


@s(auto_attribs=True)
class BuyShipment:
    has_more: Optional[bool] = None
    shipments: List[Shipment] = JList[Shipment]
