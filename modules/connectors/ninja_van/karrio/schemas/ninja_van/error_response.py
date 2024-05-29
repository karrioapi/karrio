from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class ErrorType:
    code: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class ErrorResponseType:
    transactionId: Optional[str] = None
    customerTransactionId: Optional[str] = None
    errors: List[ErrorType] = JList[ErrorType]
