import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BilledWeight:
    value: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Window:
    start: typing.Optional[str] = None
    end: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Promise:
    deliveryWindow: typing.Optional[Window] = jstruct.JStruct[Window]
    receiveWindow: typing.Optional[Window] = jstruct.JStruct[Window]


@attr.s(auto_attribs=True)
class EligibleRate:
    billedWeight: typing.Optional[BilledWeight] = jstruct.JStruct[BilledWeight]
    totalCharge: typing.Optional[BilledWeight] = jstruct.JStruct[BilledWeight]
    serviceType: typing.Optional[str] = None
    promise: typing.Optional[Promise] = jstruct.JStruct[Promise]
    rateId: typing.Optional[str] = None
    expirationTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CreateShipmentResponse:
    shipmentId: typing.Optional[str] = None
    eligibleRates: typing.Optional[typing.List[EligibleRate]] = jstruct.JList[EligibleRate]
