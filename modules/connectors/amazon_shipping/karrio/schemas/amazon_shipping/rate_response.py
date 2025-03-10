import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BillableWeight:
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
class ServiceRate:
    billableWeight: typing.Optional[BillableWeight] = jstruct.JStruct[BillableWeight]
    totalCharge: typing.Optional[BillableWeight] = jstruct.JStruct[BillableWeight]
    serviceType: typing.Optional[str] = None
    promise: typing.Optional[Promise] = jstruct.JStruct[Promise]


@attr.s(auto_attribs=True)
class RateResponse:
    serviceRates: typing.Optional[typing.List[ServiceRate]] = jstruct.JList[ServiceRate]
