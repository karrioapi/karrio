import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class HeaderType:
    ApplicationID: typing.Any = None
    AsynchronousMessageFlag: typing.Any = None
    CreateTimestamp: typing.Optional[str] = None
    DocumentType: typing.Optional[str] = None
    Environment: typing.Optional[str] = None
    MessageIdentifier: typing.Optional[str] = None
    MessageReceiver: typing.Any = None
    MessageSender: typing.Optional[str] = None
    MessageVersion: typing.Optional[str] = None
    References: typing.Any = None
    SourceSystemCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseIDType:
    Value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ResponseMessageType:
    ResponseID: typing.Optional[ResponseIDType] = jstruct.JStruct[ResponseIDType]
    ResponseMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseMessagesType:
    ResponseMessage: typing.Optional[typing.List[ResponseMessageType]] = jstruct.JList[ResponseMessageType]


@attr.s(auto_attribs=True)
class TollMessageType:
    Header: typing.Optional[HeaderType] = jstruct.JStruct[HeaderType]
    ResponseMessages: typing.Optional[ResponseMessagesType] = jstruct.JStruct[ResponseMessagesType]


@attr.s(auto_attribs=True)
class LabelResponseType:
    TollMessage: typing.Optional[TollMessageType] = jstruct.JStruct[TollMessageType]
