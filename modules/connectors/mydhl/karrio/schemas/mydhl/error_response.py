import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorResponseType:
    instance: typing.Optional[str] = None
    detail: typing.Optional[str] = None
    title: typing.Optional[str] = None
    message: typing.Optional[str] = None
    status: typing.Optional[int] = None
