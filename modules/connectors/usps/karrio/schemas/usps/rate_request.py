from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class RateRequestType:
    originZIPCode: Optional[str] = None
    destinationZIPCode: Optional[str] = None
    weight: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    mailClass: Optional[str] = None
    mailClasses: List[str] = []
    priceType: Optional[str] = None
    mailingDate: Optional[str] = None
    accountType: Optional[str] = None
    accountNumber: Optional[str] = None
    itemValue: Optional[int] = None
    extraServices: List[int] = []
