from attr import s
from typing import Optional, List, Any
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ReferenceType:
    ReferenceType: Optional[str] = None
    ReferenceValue: Optional[str] = None


@s(auto_attribs=True)
class ReferencesType:
    Reference: List[ReferenceType] = JList[ReferenceType]


@s(auto_attribs=True)
class HeaderType:
    MessageVersion: Optional[str] = None
    MessageIdentifier: Optional[str] = None
    CreateTimestamp: Optional[str] = None
    DocumentType: Optional[str] = None
    Environment: Optional[str] = None
    SourceSystemCode: Optional[str] = None
    MessageSender: Optional[str] = None
    MessageReceiver: Optional[str] = None
    ResponseStatus: Any = None
    References: Optional[ReferencesType] = JStruct[ReferencesType]


@s(auto_attribs=True)
class BaseAmountType:
    Currency: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class TransitTimeType:
    UOM: Optional[str] = None
    Value: Optional[int] = None


@s(auto_attribs=True)
class ResponseType:
    BaseAmount: Optional[BaseAmountType] = JStruct[BaseAmountType]
    GSTAmount: Optional[BaseAmountType] = JStruct[BaseAmountType]
    TotalChargeAmount: Optional[BaseAmountType] = JStruct[BaseAmountType]
    TotalSurcharges: Optional[BaseAmountType] = JStruct[BaseAmountType]
    FreightCharge: Optional[BaseAmountType] = JStruct[BaseAmountType]
    TollExtraServiceCharge: Optional[BaseAmountType] = JStruct[BaseAmountType]
    TotalFees: Optional[BaseAmountType] = JStruct[BaseAmountType]
    EnquiryID: Optional[int] = None
    TransitTime: Optional[TransitTimeType] = JStruct[TransitTimeType]


@s(auto_attribs=True)
class RateEnquiryType:
    Response: Optional[ResponseType] = JStruct[ResponseType]


@s(auto_attribs=True)
class TollMessageType:
    Header: Optional[HeaderType] = JStruct[HeaderType]
    RateEnquiry: Optional[RateEnquiryType] = JStruct[RateEnquiryType]


@s(auto_attribs=True)
class RateResponseType:
    TollMessage: Optional[TollMessageType] = JStruct[TollMessageType]
