import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AlertType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageLevelResultType:
    TrackingNumber: typing.Optional[str] = None
    Status: typing.Optional[AlertType] = jstruct.JStruct[AlertType]


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None
    TransactionIdentifier: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseType:
    ResponseStatus: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    Alert: typing.Optional[AlertType] = jstruct.JStruct[AlertType]
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class SummaryResultType:
    Status: typing.Optional[AlertType] = jstruct.JStruct[AlertType]


@attr.s(auto_attribs=True)
class VoidShipmentResponseType:
    Response: typing.Optional[ResponseType] = jstruct.JStruct[ResponseType]
    SummaryResult: typing.Optional[SummaryResultType] = jstruct.JStruct[SummaryResultType]
    PackageLevelResult: typing.Optional[typing.List[PackageLevelResultType]] = jstruct.JList[PackageLevelResultType]


@attr.s(auto_attribs=True)
class ShippingCancelResponseType:
    VoidShipmentResponse: typing.Optional[VoidShipmentResponseType] = jstruct.JStruct[VoidShipmentResponseType]
