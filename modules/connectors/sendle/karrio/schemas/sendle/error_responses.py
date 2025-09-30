import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MessagesClassType:
    pass


@attr.s(auto_attribs=True)
class ErrorResponseType:
    messages: typing.Optional[typing.Union[MessagesClassType, str]] = None
    error: typing.Optional[str] = None
    error_description: typing.Optional[str] = None
