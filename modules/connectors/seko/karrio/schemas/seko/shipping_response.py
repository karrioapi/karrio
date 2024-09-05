from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CommodityChangeType:
    OriginalDescription: Optional[str] = None
    SuitableDescription: Optional[str] = None
    OriginalHSCode: Any = None
    SuitableHsCode: Optional[int] = None


@s(auto_attribs=True)
class ItemType:
    PartNo: Optional[int] = None
    TrackingNo: Optional[str] = None
    Barcode: Optional[str] = None
    InternalBarcode: Optional[str] = None
    Charge: Optional[float] = None
    ChargeFAF: Optional[float] = None
    ChargeRural: Optional[float] = None
    ChargeSatDel: Optional[float] = None
    ChargeInsurance: Optional[float] = None
    IsTrackPack: Optional[bool] = None
    BarcodeText: Optional[str] = None
    TrackingBarcode: Optional[str] = None
    TrackingBarcode2: Optional[str] = None


@s(auto_attribs=True)
class OutputFilesType:
    LABELPDF100X150: List[str] = []


@s(auto_attribs=True)
class ConsignmentType:
    Connote: Optional[str] = None
    TrackingUrl: Optional[str] = None
    Cost: Optional[float] = None
    CarrierType: Optional[int] = None
    IsSaturdayDelivery: Optional[bool] = None
    IsRural: Optional[bool] = None
    IsOvernight: Optional[bool] = None
    HasTrackPaks: Optional[bool] = None
    ConsignmentId: Optional[int] = None
    OutputFiles: Optional[OutputFilesType] = JStruct[OutputFilesType]
    Items: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class ErrorType:
    Property: Optional[str] = None
    Message: Optional[str] = None
    Key: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class ShippingResponseType:
    CarrierId: Optional[int] = None
    CarrierName: Optional[str] = None
    IsFreightForward: Optional[bool] = None
    IsOvernight: Optional[bool] = None
    IsSaturdayDelivery: Optional[bool] = None
    IsRural: Optional[bool] = None
    HasTrackPaks: Optional[bool] = None
    Message: Optional[str] = None
    Errors: List[ErrorType] = JList[ErrorType]
    SiteId: Optional[int] = None
    Consignments: List[ConsignmentType] = JList[ConsignmentType]
    DestinationPort: Optional[str] = None
    Downloads: List[Any] = []
    CommodityChanges: List[CommodityChangeType] = JList[CommodityChangeType]
    CarrierType: Optional[int] = None
    AlertPath: Any = None
    Notifications: List[Any] = []
    InvoiceResponse: Optional[str] = None
    LogoPath: Optional[str] = None
