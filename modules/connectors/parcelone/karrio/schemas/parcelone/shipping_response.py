"""ParcelOne Shipping REST API v1 - Response Types."""

import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class FormatType:
    """Document format."""

    Type: typing.Optional[str] = None
    Size: typing.Optional[str] = None
    Unit: typing.Optional[str] = None
    Orientation: typing.Optional[int] = None
    Height: typing.Optional[str] = None
    Width: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AmountType:
    """Monetary amount."""

    Currency: typing.Optional[str] = None
    Value: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentErrorType:
    """Error information."""

    ErrorNo: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    StatusCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentWarningType:
    """Warning information."""

    WarningNo: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    StatusCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentActionResultType:
    """Result of shipment action with IDs and status."""

    ShipmentID: typing.Optional[str] = None
    ShipmentRef: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    Success: typing.Optional[int] = None
    Errors: typing.Optional[typing.List[ShipmentErrorType]] = jstruct.JList[ShipmentErrorType]
    Warnings: typing.Optional[typing.List[ShipmentWarningType]] = jstruct.JList[ShipmentWarningType]


@attr.s(auto_attribs=True)
class ShipmentPackageResultType:
    """Package result with label and tracking info."""

    ShipmentID: typing.Optional[str] = None
    PackageID: typing.Optional[int] = None
    PackageRef: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    DocType: typing.Optional[str] = None
    Format: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    Label: typing.Optional[str] = None
    TrackingURL: typing.Optional[str] = None
    CarrierTrackURL: typing.Optional[str] = None
    Charges: typing.Optional[typing.List[AmountType]] = jstruct.JList[AmountType]


@attr.s(auto_attribs=True)
class ShipmentDocumentsResultType:
    """Document result (returns, customs docs, etc)."""

    ShipmentID: typing.Optional[str] = None
    PackageID: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    DocType: typing.Optional[str] = None
    Format: typing.Optional[FormatType] = jstruct.JStruct[FormatType]
    Document: typing.Optional[str] = None
    Charges: typing.Optional[typing.List[AmountType]] = jstruct.JList[AmountType]
    PackageRef: typing.Optional[str] = None
    PackageTrackingID: typing.Optional[str] = None
    ActionResult: typing.Optional[ShipmentActionResultType] = jstruct.JStruct[ShipmentActionResultType]
    DocumentID: typing.Optional[str] = None
    Type: typing.Optional[str] = None
    Size: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentResultType:
    """Complete shipment result with labels and documents."""

    YourShipmentID: typing.Optional[str] = None
    ActionResult: typing.Optional[ShipmentActionResultType] = jstruct.JStruct[ShipmentActionResultType]
    LabelURL: typing.Optional[str] = None
    Charges: typing.Optional[typing.List[AmountType]] = jstruct.JList[AmountType]
    TotalCharges: typing.Optional[AmountType] = jstruct.JStruct[AmountType]
    PackageResults: typing.Optional[typing.List[ShipmentPackageResultType]] = jstruct.JList[ShipmentPackageResultType]
    DocumentsResults: typing.Optional[typing.List[ShipmentDocumentsResultType]] = jstruct.JList[ShipmentDocumentsResultType]
    InternationalDocumentsResults: typing.Optional[typing.List[ShipmentDocumentsResultType]] = jstruct.JList[ShipmentDocumentsResultType]
    LabelsAvailable: typing.Optional[int] = None
    DocumentsAvailable: typing.Optional[int] = None
    InternationalDocumentsAvailable: typing.Optional[int] = None
    InternationalDocumentsNeeded: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShippingResponseType:
    """Root shipping response wrapper."""

    status: typing.Optional[int] = None
    success: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    results: typing.Optional[ShipmentResultType] = jstruct.JStruct[ShipmentResultType]
    UniqId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentStatusResultType:
    """Shipment status result."""

    ActionResult: typing.Optional[ShipmentActionResultType] = jstruct.JStruct[ShipmentActionResultType]
    ShipmentStatusCode: typing.Optional[str] = None
    ShipmentStatus: typing.Optional[str] = None
    LastTrackingNo: typing.Optional[str] = None
    LastCEP: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentStatusResponseType:
    """Shipment status API response."""

    status: typing.Optional[int] = None
    success: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    results: typing.Optional[ShipmentStatusResultType] = jstruct.JStruct[ShipmentStatusResultType]
    UniqId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CancelShipmentResultType:
    """Cancel shipment result."""

    ShipmentID: typing.Optional[str] = None
    ShipmentRef: typing.Optional[str] = None
    TrackingID: typing.Optional[str] = None
    Success: typing.Optional[int] = None
    Errors: typing.Optional[typing.List[ShipmentErrorType]] = jstruct.JList[ShipmentErrorType]
    Warnings: typing.Optional[typing.List[ShipmentWarningType]] = jstruct.JList[ShipmentWarningType]


@attr.s(auto_attribs=True)
class CancelShipmentResponseType:
    """Cancel shipment API response."""

    status: typing.Optional[int] = None
    success: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    results: typing.Optional[CancelShipmentResultType] = jstruct.JStruct[CancelShipmentResultType]
    UniqId: typing.Optional[str] = None
