import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupRequestType:
    SlotReservationId: typing.Optional[str] = None
    SlotDate: typing.Optional[str] = None
    BringMyLabel: typing.Optional[bool] = None
