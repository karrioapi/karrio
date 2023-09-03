from attr import s
from typing import Optional


@s(auto_attribs=True)
class RateRequestType:
    accountNumber: Optional[str] = None
    subAccountNumber: Optional[str] = None
    processingLocation: Optional[str] = None
    recipientPostalCode: Optional[str] = None
    recipientCountryCode: Optional[str] = None
    totalPackageWeight: Optional[float] = None
    weightUnit: Optional[str] = None
    dimLength: Optional[float] = None
    dimWidth: Optional[float] = None
    dimHeight: Optional[float] = None
    dimUnit: Optional[str] = None
    productCode: Optional[str] = None
