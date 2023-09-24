from attr import s
from typing import Optional


@s(auto_attribs=True)
class ErrorResponseType:
    responseStatusCode: Optional[int] = None
    responseStatusMessage: Optional[str] = None
