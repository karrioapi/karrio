import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Error:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    errors: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    error: typing.Optional[Error] = jstruct.JStruct[Error]
