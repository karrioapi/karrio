import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ErrorType:
    ErrorNo: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    StatusCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WarningType:
    WarningNo: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    StatusCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResultsActionResultType:
    ShipmentID: typing.Optional[str] = None
    ShipmentRef: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    Success: typing.Optional[int] = None
    Errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
    Warnings: typing.Optional[typing.List[WarningType]] = jstruct.JList[WarningType]


@attr.s(auto_attribs=True)
class TotalChargesType:
    Currency: typing.Optional[str] = None
    Value: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DocumentsResultActionResultType:
    ShipmentID: typing.Optional[str] = None
    ShipmentRef: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    Success: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class FormatType:
    Type: typing.Optional[str] = None
    Size: typing.Optional[str] = None
    Unit: typing.Optional[str] = None
    Orientation: typing.Optional[int] = None
    Height: typing.Optional[int] = None
    Width: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DocumentsResultType:
    ShipmentID: typing.Optional[str] = None
    PackageID: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    DocType: typing.Optional[str] = None
    Format: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    Document: typing.Optional[str] = None
    Charges: typing.Optional[typing.List[TotalChargesType]] = jstruct.JList[TotalChargesType]
    PackageRef: typing.Optional[str] = None
    PackageTrackingID: typing.Optional[str] = None
    ActionResult: typing.Optional[DocumentsResultActionResultType] = jstruct.JStruct[DocumentsResultActionResultType]
    DocumentID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageResultType:
    ShipmentID: typing.Optional[str] = None
    PackageID: typing.Optional[str] = None
    PackageRef: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    DocType: typing.Optional[str] = None
    Format: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    Label: typing.Optional[str] = None
    TrackingURL: typing.Optional[str] = None
    CarrierTrackURL: typing.Optional[str] = None
    Charges: typing.Optional[typing.List[TotalChargesType]] = jstruct.JList[TotalChargesType]


@attr.s(auto_attribs=True)
class ResultsType:
    YourShipmentID: typing.Optional[str] = None
    ActionResult: typing.Optional[ResultsActionResultType] = jstruct.JStruct[ResultsActionResultType]
    LabelURL: typing.Optional[str] = None
    Charges: typing.Optional[typing.List[TotalChargesType]] = jstruct.JList[TotalChargesType]
    TotalCharges: typing.Optional[TotalChargesType] = jstruct.JStruct[TotalChargesType]
    PackageResults: typing.Optional[typing.List[PackageResultType]] = jstruct.JList[PackageResultType]
    DocumentsResults: typing.Optional[typing.List[DocumentsResultType]] = jstruct.JList[DocumentsResultType]
    InternationalDocumentsResults: typing.Optional[typing.List[DocumentsResultType]] = jstruct.JList[DocumentsResultType]
    LabelsAvailable: typing.Optional[int] = None
    DocumentsAvailable: typing.Optional[int] = None
    InternationalDocumentsAvailable: typing.Optional[int] = None
    InternationalDocumentsNeeded: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShippingResponseType:
    status: typing.Optional[int] = None
    success: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    UniqId: typing.Optional[str] = None
    results: typing.Optional[ResultsType] = jstruct.JStruct[ResultsType]
