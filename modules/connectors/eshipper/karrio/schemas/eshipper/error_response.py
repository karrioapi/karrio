from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class FieldErrorType:
    objectName: Optional[str] = None
    field: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class ErrorResponseType:
    type: Optional[str] = None
    message: Optional[str] = None
    code: Optional[str] = None
    fieldErrors: List[FieldErrorType] = JList[FieldErrorType]
    thirdPartyMessage: Optional[str] = None
