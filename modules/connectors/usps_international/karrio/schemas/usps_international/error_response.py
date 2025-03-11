import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class SourceType:
    parameter: typing.Optional[str] = None
    example: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErrorElementType:
    status: typing.Optional[str] = None
    code: typing.Optional[str] = None
    title: typing.Optional[str] = None
    detail: typing.Optional[str] = None
    source: typing.Optional[SourceType] = jstruct.JStruct[SourceType]


@attr.s(auto_attribs=True)
class ErrorResponseErrorType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None
    errors: typing.Optional[typing.List[ErrorElementType]] = jstruct.JList[ErrorElementType]


@attr.s(auto_attribs=True)
class ErrorResponseType:
    apiVersion: typing.Optional[str] = None
    error: typing.Optional[ErrorResponseErrorType] = jstruct.JStruct[ErrorResponseErrorType]
