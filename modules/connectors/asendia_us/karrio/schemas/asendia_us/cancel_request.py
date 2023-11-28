from attr import s
from typing import Optional


@s(auto_attribs=True)
class CancelRequestType:
    accountNumber: Optional[str] = None
    subAccountNumber: Optional[str] = None
    packageID: Optional[str] = None
