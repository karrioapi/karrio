import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    field: typing.Optional[str] = None
    details: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
    timestamp: typing.Optional[str] = None
    path: typing.Optional[str] = None
    status: typing.Optional[int] = None
