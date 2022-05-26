from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


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
class RateResponse:
    serviceRates: List[ServiceRate] = JList[ServiceRate]
