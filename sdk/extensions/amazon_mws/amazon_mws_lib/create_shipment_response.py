from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Error:
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None


@s(auto_attribs=True)
class BilledWeight:
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
class EligibleRate:
    rateId: Optional[str] = None
    totalCharge: Optional[BilledWeight] = JStruct[BilledWeight]
    billedWeight: Optional[BilledWeight] = JStruct[BilledWeight]
    expirationTime: Optional[str] = None
    serviceType: Optional[str] = None
    promise: Optional[Promise] = JStruct[Promise]


@s(auto_attribs=True)
class Payload:
    shipmentId: Optional[str] = None
    eligibleRates: List[EligibleRate] = JList[EligibleRate]


@s(auto_attribs=True)
class CreateShipmentResponse:
    payload: Optional[Payload] = JStruct[Payload]
    errors: List[Error] = JList[Error]
