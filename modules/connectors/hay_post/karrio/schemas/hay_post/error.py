from attr import s
from typing import Optional


@s(auto_attribs=True)
class ErrorType:
    key: Optional[str] = None
    name: Optional[str] = None
