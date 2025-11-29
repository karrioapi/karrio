import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MessageType:
    code: typing.Optional[int] = None
    level: typing.Optional[str] = None
    message: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    details: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    messages: typing.Optional[typing.List[MessageType]] = jstruct.JList[MessageType]
