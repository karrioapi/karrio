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
    status: typing.Optional[int] = None
    title: typing.Optional[str] = None
    type: typing.Optional[str] = None
    message: typing.Optional[str] = None
    code: typing.Optional[str] = None
    fieldErrors: typing.Optional[typing.List[FieldErrorType]] = jstruct.JList[FieldErrorType]
    thirdPartyMessage: typing.Optional[str] = None
