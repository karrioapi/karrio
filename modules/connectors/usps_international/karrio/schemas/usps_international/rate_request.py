from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class RateRequestType:
    originZIPCode: Optional[str] = None
    foreignPostalCode: Optional[str] = None
    destinationCountryCode: Optional[str] = None
    weight: Optional[int] = None
    mailingDate: Optional[str] = None
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    priceType: Optional[str] = None
    mailClass: Optional[str] = None
    accountType: Optional[str] = None
    accountNumber: Optional[str] = None
    itemValue: Optional[int] = None
    extraServices: List[int] = []
