from attr import s
from typing import Optional, Any
from jstruct import JDict


@s(auto_attribs=True)
class ErrorResponseType:
    errorcode: Optional[str] = None
    message: Optional[str] = None
    modelState: Optional[dict] = JDict[str, Any]
