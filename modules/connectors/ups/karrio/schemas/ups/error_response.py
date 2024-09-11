from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ErrorType:
    code: Optional[int] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    errors: List[ErrorType] = JList[ErrorType]


@s(auto_attribs=True)
class ErrorResponseType:
    response: Optional[ResponseType] = JStruct[ResponseType]
