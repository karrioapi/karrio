import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    error_code: typing.Optional[str] = None
    error_name: typing.Optional[str] = None
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None
    message: typing.Optional[str] = None
    field: typing.Optional[str] = None
    context: typing.Optional[typing.List[typing.Any]] = None
    messages: typing.Optional[typing.List[typing.Any]] = None
    error: typing.Optional[str] = None
    error_description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
