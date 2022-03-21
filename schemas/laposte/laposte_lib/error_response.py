from attr import s
from typing import Optional


@s(auto_attribs=True)
class ErrorResponse:
    lang: Optional[str] = None
    scope: Optional[str] = None
    returnCode: Optional[int] = None
    returnMessage: Optional[str] = None
    idShip: Optional[str] = None
