from attr import s
from typing import Optional, List


@s(auto_attribs=True)
class PickupRequestType:
    courier_id: Optional[str] = None
    easyship_shipment_ids: List[str] = []
    selected_date: Optional[str] = None
    selected_from_time: Optional[str] = None
    selected_to_time: Optional[str] = None
    time_slot_id: Optional[str] = None
