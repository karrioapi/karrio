from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class AccountNumberType:
    value: Optional[str] = None


@s(auto_attribs=True)
class CancelRequestType:
    accountNumber: Optional[AccountNumberType] = JStruct[AccountNumberType]
    emailShipment: Optional[bool] = None
    senderCountryCode: Optional[str] = None
    deletionControl: Optional[str] = None
    trackingNumber: Optional[str] = None
