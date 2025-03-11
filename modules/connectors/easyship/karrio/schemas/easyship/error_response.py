import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[str] = None
    details: typing.Optional[typing.List[str]] = None
    message: typing.Optional[str] = None
    request_id: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    error: typing.Optional[ErrorType] = jstruct.JStruct[ErrorType]
