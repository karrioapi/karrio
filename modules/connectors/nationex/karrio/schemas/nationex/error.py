import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    code: typing.Optional[int] = None
    message: typing.Optional[str] = None
