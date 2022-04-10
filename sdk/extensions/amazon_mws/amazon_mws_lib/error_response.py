from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None


@s(auto_attribs=True)
class ErrorResponse:
    errors: List[Error] = JList[Error]
