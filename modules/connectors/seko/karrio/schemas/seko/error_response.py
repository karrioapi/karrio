from attr import s
from typing import Optional


@s(auto_attribs=True)
class ErrorResponseType:
    Property: Optional[str] = None
    Message: Optional[str] = None
    Key: Optional[str] = None
    Value: Optional[str] = None
