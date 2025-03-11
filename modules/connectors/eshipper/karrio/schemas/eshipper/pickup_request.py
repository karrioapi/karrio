import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TimeType:
    hour: typing.Optional[int] = None
    minute: typing.Optional[int] = None
    second: typing.Optional[int] = None
    nano: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupRequestType:
    contactName: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    pickupDate: typing.Optional[str] = None
    pickupTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    closingTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    palletPickupTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    palletClosingTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    palletDeliveryClosingTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    location: typing.Optional[str] = None
    instructions: typing.Optional[str] = None
