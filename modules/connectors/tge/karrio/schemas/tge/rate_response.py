import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ReferenceType:
    ReferenceType: typing.Optional[str] = None
    ReferenceValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReferencesType:
    Reference: typing.Optional[typing.List[ReferenceType]] = jstruct.JList[ReferenceType]


@attr.s(auto_attribs=True)
class HeaderType:
    MessageVersion: typing.Optional[str] = None
    MessageIdentifier: typing.Optional[str] = None
    CreateTimestamp: typing.Optional[str] = None
    DocumentType: typing.Optional[str] = None
    Environment: typing.Optional[str] = None
    SourceSystemCode: typing.Optional[str] = None
    MessageSender: typing.Optional[str] = None
    MessageReceiver: typing.Optional[str] = None
    ResponseStatus: typing.Any = None
    References: typing.Optional[ReferencesType] = jstruct.JStruct[ReferencesType]


@attr.s(auto_attribs=True)
class BaseAmountType:
    Currency: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TransitTimeType:
    UOM: typing.Optional[str] = None
    Value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ResponseType:
    BaseAmount: typing.Optional[BaseAmountType] = jstruct.JStruct[BaseAmountType]
    GSTAmount: typing.Optional[BaseAmountType] = jstruct.JStruct[BaseAmountType]
    TotalChargeAmount: typing.Optional[BaseAmountType] = jstruct.JStruct[BaseAmountType]
    TotalSurcharges: typing.Optional[BaseAmountType] = jstruct.JStruct[BaseAmountType]
    FreightCharge: typing.Optional[BaseAmountType] = jstruct.JStruct[BaseAmountType]
    TollExtraServiceCharge: typing.Optional[BaseAmountType] = jstruct.JStruct[BaseAmountType]
    TotalFees: typing.Optional[BaseAmountType] = jstruct.JStruct[BaseAmountType]
    EnquiryID: typing.Optional[int] = None
    TransitTime: typing.Optional[TransitTimeType] = jstruct.JStruct[TransitTimeType]


@attr.s(auto_attribs=True)
class RateEnquiryType:
    Response: typing.Optional[ResponseType] = jstruct.JStruct[ResponseType]


@attr.s(auto_attribs=True)
class TollMessageType:
    Header: typing.Optional[HeaderType] = jstruct.JStruct[HeaderType]
    RateEnquiry: typing.Optional[RateEnquiryType] = jstruct.JStruct[RateEnquiryType]


@attr.s(auto_attribs=True)
class RateResponseType:
    TollMessage: typing.Optional[TollMessageType] = jstruct.JStruct[TollMessageType]
