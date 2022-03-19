from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None


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
    value: Optional[int] = None
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
    totalCharge: Optional[BillableWeight] = JStruct[BillableWeight]
    billableWeight: Optional[BillableWeight] = JStruct[BillableWeight]
    serviceType: Optional[str] = None
    promise: Optional[Promise] = JStruct[Promise]


@s(auto_attribs=True)
class Payload:
    shipmentId: Optional[str] = None
    serviceRate: Optional[ServiceRate] = JStruct[ServiceRate]
    labelResults: List[LabelResult] = JList[LabelResult]


@s(auto_attribs=True)
class PurchaseShipmentResponse:
    payload: Optional[Payload] = JStruct[Payload]
    errors: List[Error] = JList[Error]
