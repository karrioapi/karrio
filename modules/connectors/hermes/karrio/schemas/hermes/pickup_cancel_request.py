import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupCancelRequestType:
    pickupOrderID: typing.Optional[str] = None
