from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class AlertType:
    code: Optional[str] = None
    alertType: Optional[str] = None
    message: Optional[str] = None


@s(auto_attribs=True)
class OutputType:
    pickupConfirmationCode: Optional[str] = None
    cancelConfirmationMessage: Optional[str] = None
    alerts: List[AlertType] = JList[AlertType]


@s(auto_attribs=True)
class CancelPickupResponseType:
    transactionId: Optional[str] = None
    customerTransactionId: Optional[str] = None
    output: Optional[OutputType] = JStruct[OutputType]
