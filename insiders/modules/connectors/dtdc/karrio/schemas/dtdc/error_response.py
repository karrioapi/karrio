import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DatumType:
    reason: typing.Optional[str] = None
    success: typing.Optional[bool] = None
    message: typing.Optional[str] = None
    referencenumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorClassType:
    message: typing.Optional[str] = None
    statusCode: typing.Optional[int] = None
    reason: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorDetailType:
    name: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseElementType:
    status: typing.Optional[typing.Union[int, str]] = None
    data: typing.Optional[typing.List[DatumType]] = jstruct.JList[DatumType]
    success: typing.Optional[bool] = None
    message: typing.Optional[str] = None
    errorDetails: typing.Optional[typing.List[ErrorDetailType]] = jstruct.JList[ErrorDetailType]
    error: typing.Optional[typing.Union[ErrorClassType, str]] = None
    timestamp: typing.Optional[str] = None
    path: typing.Optional[str] = None
    code: typing.Optional[str] = None
    reason: typing.Optional[str] = None
