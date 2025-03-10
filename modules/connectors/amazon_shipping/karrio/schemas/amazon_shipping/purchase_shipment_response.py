import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelSpecification:
    labelFormat: typing.Optional[str] = None
    labelStockSize: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Label:
    labelStream: typing.Optional[str] = None
    labelSpecification: typing.Optional[LabelSpecification] = jstruct.JStruct[LabelSpecification]


@attr.s(auto_attribs=True)
class LabelResult:
    containerReferenceId: typing.Optional[str] = None
    trackingId: typing.Optional[str] = None
    label: typing.Optional[Label] = jstruct.JStruct[Label]


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
class PurchaseShipmentResponse:
    shipmentId: typing.Optional[str] = None
    serviceRate: typing.Optional[ServiceRate] = jstruct.JStruct[ServiceRate]
    labelResults: typing.Optional[typing.List[LabelResult]] = jstruct.JList[LabelResult]
