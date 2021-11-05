from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class ShippingCloseDispatchRequest:
    accountNumber: Optional[str] = None
    subAccountNumber: Optional[str] = None
    dispatchNumber: List[str] = JList[str]
