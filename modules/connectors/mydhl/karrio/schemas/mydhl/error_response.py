from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class ErrorResponseType:
    instance: Optional[str] = None
    detail: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    status: Optional[int] = None
    code: Optional[int] = None
    additionalDetails: List[str] = []
