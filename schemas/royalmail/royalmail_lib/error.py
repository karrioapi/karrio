import attr
from typing import Optional, List
from jstruct import JList


@attr.s(auto_attribs=True)
class Error:
    errorCode: Optional[str] = None
    errorDescription: Optional[str] = None
    errorCause: Optional[str] = None
    errorResolution: Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    httpCode: Optional[int] = None
    httpMessage: Optional[str] = None
    moreInformation: Optional[str] = None
    errors: Optional[List[Error]] = JList[Error]
