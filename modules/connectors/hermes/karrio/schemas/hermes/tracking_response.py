import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TimeSlotType:
    timeSlotfrom: typing.Optional[str] = None
    to: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryForecastType:
    fixed: typing.Optional[bool] = None
    date: typing.Optional[str] = None
    timeSlot: typing.Optional[TimeSlotType] = jstruct.JStruct[TimeSlotType]


@attr.s(auto_attribs=True)
class ReceiverAddressType:
    city: typing.Optional[str] = None
    zipCode: typing.Optional[int] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResultType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ScanningUnitType:
    name: typing.Optional[str] = None
    city: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatusType:
    timestamp: typing.Optional[str] = None
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    scanningUnit: typing.Optional[ScanningUnitType] = jstruct.JStruct[ScanningUnitType]


@attr.s(auto_attribs=True)
class ShipmentinfoType:
    shipmentID: typing.Optional[str] = None
    partNumber: typing.Optional[int] = None
    clientID: typing.Optional[int] = None
    clientReference: typing.Optional[str] = None
    clientReference2: typing.Optional[int] = None
    internationalShipmentID: typing.Optional[str] = None
    trackingLink: typing.Optional[str] = None
    result: typing.Optional[ResultType] = jstruct.JStruct[ResultType]
    receiverAddress: typing.Optional[ReceiverAddressType] = jstruct.JStruct[ReceiverAddressType]
    deliveryForecast: typing.Optional[DeliveryForecastType] = jstruct.JStruct[DeliveryForecastType]
    status: typing.Optional[typing.List[StatusType]] = jstruct.JList[StatusType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    shipmentinfo: typing.Optional[typing.List[ShipmentinfoType]] = jstruct.JList[ShipmentinfoType]
