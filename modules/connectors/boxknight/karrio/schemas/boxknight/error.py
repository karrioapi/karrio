import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Error:
    error: typing.Optional[str] = None
