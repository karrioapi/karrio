from attr import s
from typing import Optional, Any, Union, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ContextType:
    pass


@s(auto_attribs=True)
class ErrorType:
    error_code: Optional[str] = None
    error_name: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    message: Optional[str] = None
    error_description: Optional[str] = None
    field: Optional[str] = None
    context: Optional[ContextType] = JStruct[ContextType]
    messages: Union[ContextType, Any, str]
    error: Optional[str] = None


@s(auto_attribs=True)
class ErrorResponseType:
    errors: List[ErrorType] = JList[ErrorType]
