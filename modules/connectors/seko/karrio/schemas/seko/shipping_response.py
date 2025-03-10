import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CommodityChangeType:
    OriginalDescription: typing.Optional[str] = None
    SuitableDescription: typing.Optional[str] = None
    OriginalHSCode: typing.Any = None
    SuitableHsCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ItemType:
    PartNo: typing.Optional[int] = None
    TrackingNo: typing.Optional[str] = None
    Barcode: typing.Optional[str] = None
    InternalBarcode: typing.Optional[str] = None
    Charge: typing.Optional[float] = None
    ChargeFAF: typing.Optional[float] = None
    ChargeRural: typing.Optional[float] = None
    ChargeSatDel: typing.Optional[float] = None
    ChargeInsurance: typing.Optional[float] = None
    IsTrackPack: typing.Optional[bool] = None
    BarcodeText: typing.Optional[str] = None
    TrackingBarcode: typing.Optional[str] = None
    TrackingBarcode2: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OutputFilesType:
    LABELPDF100X150: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ConsignmentType:
    Connote: typing.Optional[str] = None
    TrackingUrl: typing.Optional[str] = None
    Cost: typing.Optional[float] = None
    CarrierType: typing.Optional[int] = None
    IsSaturdayDelivery: typing.Optional[bool] = None
    IsRural: typing.Optional[bool] = None
    IsOvernight: typing.Optional[bool] = None
    HasTrackPaks: typing.Optional[bool] = None
    ConsignmentId: typing.Optional[int] = None
    OutputFiles: typing.Optional[OutputFilesType] = jstruct.JStruct[OutputFilesType]
    Items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]


@attr.s(auto_attribs=True)
class ErrorType:
    Property: typing.Optional[str] = None
    Message: typing.Optional[str] = None
    Key: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingResponseType:
    CarrierId: typing.Optional[int] = None
    CarrierName: typing.Optional[str] = None
    IsFreightForward: typing.Optional[bool] = None
    IsOvernight: typing.Optional[bool] = None
    IsSaturdayDelivery: typing.Optional[bool] = None
    IsRural: typing.Optional[bool] = None
    HasTrackPaks: typing.Optional[bool] = None
    Message: typing.Optional[str] = None
    Errors: typing.Optional[typing.List[ErrorType]] = jstruct.JList[ErrorType]
    SiteId: typing.Optional[int] = None
    Consignments: typing.Optional[typing.List[ConsignmentType]] = jstruct.JList[ConsignmentType]
    DestinationPort: typing.Optional[str] = None
    Downloads: typing.Optional[typing.List[typing.Any]] = None
    CommodityChanges: typing.Optional[typing.List[CommodityChangeType]] = jstruct.JList[CommodityChangeType]
    CarrierType: typing.Optional[int] = None
    AlertPath: typing.Any = None
    Notifications: typing.Optional[typing.List[typing.Any]] = None
    InvoiceResponse: typing.Optional[str] = None
    LogoPath: typing.Optional[str] = None
