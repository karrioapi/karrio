from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


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
class BillableWeight:
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
class ServiceRate:
    billableWeight: Optional[BillableWeight] = JStruct[BillableWeight]
    totalCharge: Optional[BillableWeight] = JStruct[BillableWeight]
    serviceType: Optional[str] = None
    promise: Optional[Promise] = JStruct[Promise]


@s(auto_attribs=True)
class PurchaseShipmentResponse:
    shipmentId: Optional[str] = None
    serviceRate: Optional[ServiceRate] = JStruct[ServiceRate]
    labelResults: List[LabelResult] = JList[LabelResult]
