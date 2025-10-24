import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseType:
    errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]


@attr.s(auto_attribs=True)
class ErrorResponseType:
    response: typing.Optional[ResponseType] = jstruct.JStruct[ResponseType]
