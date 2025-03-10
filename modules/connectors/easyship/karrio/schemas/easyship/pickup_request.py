import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PickupRequestType:
    courier_id: typing.Optional[str] = None
    easyship_shipment_ids: typing.Optional[typing.List[str]] = None
    selected_date: typing.Optional[str] = None
    selected_from_time: typing.Optional[str] = None
    selected_to_time: typing.Optional[str] = None
    time_slot_id: typing.Optional[str] = None
