from attr import s
from typing import Optional


@s(auto_attribs=True)
class RateResponse:
    price: Optional[float] = None
    size: Optional[str] = None
    estimated_distance: Optional[float] = None
