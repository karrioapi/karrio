from attr import s
from typing import Optional


@s(auto_attribs=True)
class ErrorType:
    code: Optional[int] = None
    message: Optional[str] = None
