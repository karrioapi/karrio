from attr import s
from typing import Optional, Any, List
from jstruct import JStruct


@s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    message: Optional[str] = None
    errors: List[Any] = []


@s(auto_attribs=True)
class ErrorResponse:
    error: Optional[Error] = JStruct[Error]
