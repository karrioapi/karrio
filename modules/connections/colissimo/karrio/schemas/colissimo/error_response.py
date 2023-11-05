from attr import s
from typing import Optional


@s(auto_attribs=True)
class ErrorResponse:
    returnCode: Optional[int] = None
    returnMessage: Optional[str] = None
    lang: Optional[str] = None
    scope: Optional[str] = None
    idShip: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
