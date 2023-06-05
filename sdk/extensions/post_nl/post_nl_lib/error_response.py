from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ErrorType:
    ErrorCode: Optional[int] = None
    ErrorDescription: Optional[str] = None
    Error: Optional[str] = None
    Code: Optional[int] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class DetailType:
    errorcode: Optional[str] = None


@s(auto_attribs=True)
class FaultType:
    faultstring: Optional[str] = None
    detail: Optional[DetailType] = JStruct[DetailType]


@s(auto_attribs=True)
class ErrorResponseType:
    Date: Optional[str] = None
    Error: Optional[ErrorType] = JStruct[ErrorType]
    RequestId: Optional[str] = None
    Errors: List[ErrorType] = JList[ErrorType]
    fault: Optional[FaultType] = JStruct[FaultType]
