from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class ErrorElement:
    code: Optional[int] = None
    parameter: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class Error:
    errors: List[ErrorElement] = JList[ErrorElement]
