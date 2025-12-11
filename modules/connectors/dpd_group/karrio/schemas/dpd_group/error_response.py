import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorResponseType:
    errorCode: typing.Optional[str] = None
    errorMessage: typing.Optional[str] = None
    errorOrigin: typing.Optional[str] = None
