from attr import s
from typing import Optional, List, Any
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ErrorNumberType:
    Value: Optional[str] = None


@s(auto_attribs=True)
class ErrorMessageType:
    ErrorMessage: Optional[str] = None
    ErrorNumber: Optional[ErrorNumberType] = JStruct[ErrorNumberType]


@s(auto_attribs=True)
class ErrorMessagesType:
    ErrorMessage: List[ErrorMessageType] = JList[ErrorMessageType]


@s(auto_attribs=True)
class HeaderType:
    ApplicationID: Any = None
    AsynchronousMessageFlag: Any = None
    CreateTimestamp: Optional[str] = None
    DocumentType: Optional[str] = None
    Environment: Optional[str] = None
    MessageIdentifier: Optional[str] = None
    MessageReceiver: Any = None
    MessageSender: Optional[str] = None
    MessageVersion: Optional[str] = None
    References: Any = None
    SourceSystemCode: Optional[str] = None


@s(auto_attribs=True)
class TollMessageType:
    ErrorMessages: Optional[ErrorMessagesType] = JStruct[ErrorMessagesType]
    Header: Optional[HeaderType] = JStruct[HeaderType]


@s(auto_attribs=True)
class ErrorResponseType:
    TollMessage: Optional[TollMessageType] = JStruct[TollMessageType]
    ExceptionMessage: Optional[str] = None
    message: Optional[str] = None
