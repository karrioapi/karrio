from attr import s
from typing import Optional


@s(auto_attribs=True)
class ErrorResponseType:
    title: Optional[str] = None
    statusCode: Optional[int] = None
    instance: Optional[str] = None
    detail: Optional[str] = None
