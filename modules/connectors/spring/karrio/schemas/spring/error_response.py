import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorResponseType:
    ErrorLevel: typing.Optional[int] = None
    Error: typing.Optional[str] = None
