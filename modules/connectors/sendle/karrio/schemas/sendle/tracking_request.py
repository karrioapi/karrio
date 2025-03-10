import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingRequestType:
    ref: typing.Optional[int] = None
