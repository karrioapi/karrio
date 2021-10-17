from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class InvalidParam:
    name: Optional[str] = None
    path: Optional[str] = None
    reason: Optional[str] = None


@s(auto_attribs=True)
class Error:
    type: Optional[str] = None
    title: Optional[str] = None
    invalidParams: List[InvalidParam] = JList[InvalidParam]
