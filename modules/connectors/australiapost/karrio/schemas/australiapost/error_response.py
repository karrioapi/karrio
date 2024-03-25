from attr import s
from typing import Optional, Any, List
from jstruct import JList


@s(auto_attribs=True)
class ErrorType:
    error_code: Optional[str] = None
    error_name: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    message: Optional[str] = None
    field: Optional[str] = None
    context: List[Any] = []
    messages: List[Any] = []
    error: Optional[str] = None
    error_description: Optional[str] = None


@s(auto_attribs=True)
class ErrorResponseType:
    errors: List[ErrorType] = JList[ErrorType]
