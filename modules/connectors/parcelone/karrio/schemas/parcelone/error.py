import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    ErrorNo: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    StatusCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    status: typing.Optional[int] = None
    success: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
    UniqId: typing.Optional[str] = None
