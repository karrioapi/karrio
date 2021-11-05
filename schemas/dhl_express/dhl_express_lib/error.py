from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class InvalidParameter:
    instance: Optional[str] = None
    title: Optional[str] = None
    detail: Optional[str] = None
    code: Optional[int] = None


@s(auto_attribs=True)
class Error:
    title: Optional[str] = None
    detail: Optional[str] = None
    invalidParameters: List[InvalidParameter] = JList[InvalidParameter]
