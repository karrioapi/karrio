import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DetailType:
    field: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    details: typing.Optional[typing.List[DetailType]] = jstruct.JList[DetailType]


@attr.s(auto_attribs=True)
class ErrorResponseType:
    error: typing.Optional[ErrorType] = jstruct.JStruct[ErrorType]
    timestamp: typing.Optional[str] = None
    path: typing.Optional[str] = None
    status: typing.Optional[int] = None
