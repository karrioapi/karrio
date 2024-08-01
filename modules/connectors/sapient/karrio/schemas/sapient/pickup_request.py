from attr import s
from typing import Optional


@s(auto_attribs=True)
class PickupRequestType:
    SlotReservationId: Optional[str] = None
    SlotDate: Optional[str] = None
    BringMyLabel: Optional[bool] = None
