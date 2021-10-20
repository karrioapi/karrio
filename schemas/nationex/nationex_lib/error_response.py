from attr import s
from typing import Optional


@s(auto_attribs=True)
class ErrorResponse:
    code: Optional[int] = None
    message: Optional[str] = None
