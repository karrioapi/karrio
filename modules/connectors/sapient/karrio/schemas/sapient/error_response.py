from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class ErrorType:
    Message: Optional[str] = None
    Cause: Optional[str] = None
    ErrorCode: Optional[str] = None


@s(auto_attribs=True)
class ErrorResponseType:
    Message: Optional[str] = None
    Errors: List[ErrorType] = JList[ErrorType]
