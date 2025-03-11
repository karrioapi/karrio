import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorNumberType:
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorMessageType:
    ErrorMessage: typing.Optional[str] = None
    ErrorNumber: typing.Optional[ErrorNumberType] = jstruct.JStruct[ErrorNumberType]


@attr.s(auto_attribs=True)
class ErrorMessagesType:
    ErrorMessage: typing.Optional[typing.List[ErrorMessageType]] = jstruct.JList[ErrorMessageType]


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
class TollMessageType:
    ErrorMessages: typing.Optional[ErrorMessagesType] = jstruct.JStruct[ErrorMessagesType]
    Header: typing.Optional[HeaderType] = jstruct.JStruct[HeaderType]


@attr.s(auto_attribs=True)
class ErrorResponseType:
    TollMessage: typing.Optional[TollMessageType] = jstruct.JStruct[TollMessageType]
    Exception: typing.Optional[str] = None
    ExceptionMessage: typing.Optional[str] = None
    message: typing.Optional[str] = None
