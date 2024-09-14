from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class ErrorType:
    code: Optional[str] = None
    details: List[str] = []
    message: Optional[str] = None
    requestid: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class ErrorResponseType:
    error: Optional[ErrorType] = JStruct[ErrorType]
