import attr
from jstruct import JList
from typing import Optional, List


@attr.s(auto_attribs=True)
class Rate:
    price: Optional[int] = None
    name: Optional[str] = None
    service: Optional[str] = None
    description: Optional[str] = None
    estimateDay: Optional[str] = None
    estimateFrom: Optional[str] = None
    estimateTo: Optional[str] = None


@attr.s(auto_attribs=True)
class RateRequest:
    postalCode: str
    originPostalCode: str


@attr.s(auto_attribs=True)
class RateResponse:
    rates: List[Rate] = JList[Rate]
