from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class SourceType:
    parameter: Optional[str] = None
    example: Optional[str] = None


@s(auto_attribs=True)
class ErrorElementType:
    status: Optional[str] = None
    code: Optional[str] = None
    title: Optional[str] = None
    detail: Optional[str] = None
    source: Optional[SourceType] = JStruct[SourceType]


@s(auto_attribs=True)
class ErrorResponseErrorType:
    code: Optional[str] = None
    message: Optional[str] = None
    errors: List[ErrorElementType] = JList[ErrorElementType]


@s(auto_attribs=True)
class ErrorResponseType:
    apiVersion: Optional[str] = None
    error: Optional[ErrorResponseErrorType] = JStruct[ErrorResponseErrorType]
