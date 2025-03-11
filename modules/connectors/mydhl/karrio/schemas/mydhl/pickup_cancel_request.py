import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupCancelRequestType:
    requestorName: typing.Optional[str] = None
    reason: typing.Optional[str] = None
