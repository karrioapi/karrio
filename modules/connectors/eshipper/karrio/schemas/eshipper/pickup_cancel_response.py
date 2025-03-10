import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupCancelResponseType:
    orderId: typing.Optional[int] = None
    status: typing.Optional[str] = None
