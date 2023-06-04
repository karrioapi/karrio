from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AlertType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class PackageLevelResultType:
    TrackingNumber: Optional[str] = None
    Status: Optional[AlertType] = JStruct[AlertType]


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None
    TransactionIdentifier: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    ResponseStatus: Optional[AlertType] = JStruct[AlertType]
    Alert: Optional[AlertType] = JStruct[AlertType]
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class SummaryResultType:
    Status: Optional[AlertType] = JStruct[AlertType]


@s(auto_attribs=True)
class VoidShipmentResponseType:
    Response: Optional[ResponseType] = JStruct[ResponseType]
    SummaryResult: Optional[SummaryResultType] = JStruct[SummaryResultType]
    PackageLevelResult: List[PackageLevelResultType] = JList[PackageLevelResultType]


@s(auto_attribs=True)
class ShippingCancelResponseType:
    VoidShipmentResponse: Optional[VoidShipmentResponseType] = JStruct[VoidShipmentResponseType]
