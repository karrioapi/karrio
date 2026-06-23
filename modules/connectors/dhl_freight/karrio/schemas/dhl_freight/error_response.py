import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class InvalidParamType:
    name: typing.Optional[str] = None
    reason: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValidationErrorType:
    errorCode: typing.Optional[int] = None
    message: typing.Optional[str] = None
    field: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    status: typing.Optional[str] = None
    validationErrors: typing.Optional[typing.List[ValidationErrorType]] = jstruct.JList[ValidationErrorType]
    type: typing.Optional[str] = None
    title: typing.Optional[str] = None
    statusCode: typing.Optional[int] = None
    detail: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    error: typing.Optional[str] = None
    errordescription: typing.Optional[str] = None
    invalidParams: typing.Optional[typing.List[InvalidParamType]] = jstruct.JList[InvalidParamType]
