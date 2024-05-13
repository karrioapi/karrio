from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class TimeType:
    hour: Optional[int] = None
    minute: Optional[int] = None
    second: Optional[int] = None
    nano: Optional[int] = None


@s(auto_attribs=True)
class PickupRequestType:
    contactName: Optional[str] = None
    phoneNumber: Optional[str] = None
    pickupDate: Optional[str] = None
    pickupTime: Optional[TimeType] = JStruct[TimeType]
    closingTime: Optional[TimeType] = JStruct[TimeType]
    palletPickupTime: Optional[TimeType] = JStruct[TimeType]
    palletClosingTime: Optional[TimeType] = JStruct[TimeType]
    palletDeliveryClosingTime: Optional[TimeType] = JStruct[TimeType]
    location: Optional[str] = None
    instructions: Optional[str] = None
