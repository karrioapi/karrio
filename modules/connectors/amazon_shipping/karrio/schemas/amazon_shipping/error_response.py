import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Error:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    details: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    errors: typing.Optional[typing.List[Error]] = jstruct.JList[Error]
