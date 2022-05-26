from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class BilledWeight:
    value: Optional[float] = None
    unit: Optional[str] = None


@s(auto_attribs=True)
class Window:
    start: Optional[str] = None
    end: Optional[str] = None


@s(auto_attribs=True)
class Promise:
    deliveryWindow: Optional[Window] = JStruct[Window]
    receiveWindow: Optional[Window] = JStruct[Window]


@s(auto_attribs=True)
class AcceptedRate:
    billedWeight: Optional[BilledWeight] = JStruct[BilledWeight]
    totalCharge: Optional[BilledWeight] = JStruct[BilledWeight]
    serviceType: Optional[str] = None
    promise: Optional[Promise] = JStruct[Promise]


@s(auto_attribs=True)
class LabelSpecification:
    labelFormat: Optional[str] = None
    labelStockSize: Optional[str] = None


@s(auto_attribs=True)
class Label:
    labelStream: Optional[str] = None
    labelSpecification: Optional[LabelSpecification] = JStruct[LabelSpecification]


@s(auto_attribs=True)
class LabelResult:
    containerReferenceId: Optional[str] = None
    trackingId: Optional[str] = None
    label: Optional[Label] = JStruct[Label]


@s(auto_attribs=True)
class PurchaseLabelResponse:
    shipmentId: Optional[str] = None
    clientReferenceId: Optional[str] = None
    acceptedRate: Optional[AcceptedRate] = JStruct[AcceptedRate]
    labelResults: List[LabelResult] = JList[LabelResult]
