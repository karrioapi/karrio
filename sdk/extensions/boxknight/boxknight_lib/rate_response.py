from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class Rate:
    price: Optional[int] = None
    service: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    estimateDay: Optional[str] = None
    estimateFrom: Optional[str] = None
    estimateTo: Optional[str] = None


@s(auto_attribs=True)
class RateResponse:
    rates: List[Rate] = JList[Rate]
