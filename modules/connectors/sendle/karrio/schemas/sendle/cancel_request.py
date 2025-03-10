import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CancelRequestType:
    id: typing.Optional[int] = None
