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
class EligibleRate:
    billedWeight: Optional[BilledWeight] = JStruct[BilledWeight]
    totalCharge: Optional[BilledWeight] = JStruct[BilledWeight]
    serviceType: Optional[str] = None
    promise: Optional[Promise] = JStruct[Promise]
    rateId: Optional[str] = None
    expirationTime: Optional[str] = None


@s(auto_attribs=True)
class CreateShipmentResponse:
    shipmentId: Optional[str] = None
    eligibleRates: List[EligibleRate] = JList[EligibleRate]
