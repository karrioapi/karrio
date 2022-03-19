from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None


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
    serviceRates: List[ServiceRate] = JList[ServiceRate]


@s(auto_attribs=True)
class RateResponse:
    payload: Optional[Payload] = JStruct[Payload]
    errors: List[Error] = JList[Error]
