import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    Message: typing.Optional[str] = None
    Cause: typing.Optional[str] = None
    ErrorCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    Message: typing.Optional[str] = None
    Errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
