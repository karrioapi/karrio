import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    key: typing.Optional[str] = None
    name: typing.Optional[str] = None
