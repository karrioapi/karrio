from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ErrorElementType:
    code: Optional[int] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    errors: List[ErrorElementType] = JList[ErrorElementType]


@s(auto_attribs=True)
class ErrorType:
    response: Optional[ResponseType] = JStruct[ResponseType]
