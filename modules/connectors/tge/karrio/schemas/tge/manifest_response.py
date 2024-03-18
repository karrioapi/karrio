from attr import s
from typing import Any, Optional, List
from jstruct import JStruct, JList


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
class ResponseIDType:
    Value: Optional[int] = None


@s(auto_attribs=True)
class ResponseMessageType:
    ResponseID: Optional[ResponseIDType] = JStruct[ResponseIDType]
    ResponseMessage: Optional[str] = None


@s(auto_attribs=True)
class ResponseMessagesType:
    ResponseMessage: List[ResponseMessageType] = JList[ResponseMessageType]


@s(auto_attribs=True)
class TollMessageType:
    Header: Optional[HeaderType] = JStruct[HeaderType]
    ResponseMessages: Optional[ResponseMessagesType] = JStruct[ResponseMessagesType]


@s(auto_attribs=True)
class ManifestResponseType:
    TollMessage: Optional[TollMessageType] = JStruct[TollMessageType]
