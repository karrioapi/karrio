import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class FieldErrorType:
    objectName: typing.Optional[str] = None
    field: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorResponseType:
    type: typing.Optional[str] = None
    title: typing.Optional[str] = None
    status: typing.Optional[int] = None
    detail: typing.Optional[str] = None
    path: typing.Optional[str] = None
    message: typing.Optional[str] = None
    fieldErrors: typing.Optional[typing.List[FieldErrorType]] = jstruct.JList[FieldErrorType]
