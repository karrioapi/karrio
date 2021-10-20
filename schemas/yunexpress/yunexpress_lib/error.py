import attr
from jstruct import JStruct, JList
from typing import Optional, List


@attr.s(auto_attribs=True)
class ErrorResponse:
    Message: Optional[str] = None
    MessageDetail: Optional[str] = None
    ResultCode: Optional[int] = None
    ResultDesc: Optional[str] = None
