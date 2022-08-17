from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class AlertType:
    Code: Optional[int] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None
    TransactionIdentifier: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    ResponseStatus: Optional[str] = None
    Alert: List[AlertType] = JList[AlertType]
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class FreightCancelPickupResponseClassType:
    Response: Optional[ResponseType] = JStruct[ResponseType]
    FreightCancelStatus: Optional[str] = None


@s(auto_attribs=True)
class FreightCancelPickupResponseType:
    FreightCancelPickupResponse: Optional[FreightCancelPickupResponseClassType] = JStruct[FreightCancelPickupResponseClassType]
