import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorResponseType:
    title: typing.Optional[str] = None
    statusCode: typing.Optional[int] = None
    instance: typing.Optional[str] = None
    detail: typing.Optional[str] = None
