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
class AcceptedRate:
    billedWeight: typing.Optional[BilledWeight] = jstruct.JStruct[BilledWeight]
    totalCharge: typing.Optional[BilledWeight] = jstruct.JStruct[BilledWeight]
    serviceType: typing.Optional[str] = None
    promise: typing.Optional[Promise] = jstruct.JStruct[Promise]


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
class PurchaseLabelResponse:
    shipmentId: typing.Optional[str] = None
    clientReferenceId: typing.Optional[str] = None
    acceptedRate: typing.Optional[AcceptedRate] = jstruct.JStruct[AcceptedRate]
    labelResults: typing.Optional[typing.List[LabelResult]] = jstruct.JList[LabelResult]
