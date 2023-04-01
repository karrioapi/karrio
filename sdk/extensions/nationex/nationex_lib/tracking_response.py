from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccessoryType:
    InsuranceAmount: Optional[int] = None
    FrozenProtection: Optional[bool] = None
    DangerousGoods: Optional[bool] = None
    SNR: Optional[bool] = None


@s(auto_attribs=True)
class DestinationType:
    Contact: Optional[str] = None
    AccountNumber: Optional[str] = None
    AccountName: Optional[str] = None
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    PostalCode: Optional[str] = None
    City: Optional[str] = None
    ProvinceState: Optional[str] = None
    Phone: Optional[str] = None
    SmsNotification: Optional[bool] = None
    EmailNotification: Optional[bool] = None
    NoCivic: Optional[int] = None
    Suite: Optional[int] = None
    StreetName: Optional[str] = None
    Email: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    Height: Optional[float] = None
    Length: Optional[int] = None
    Width: Optional[int] = None
    Cubing: Optional[float] = None


@s(auto_attribs=True)
class GeocodingType:
    Longitude: Optional[float] = None
    Latitude: Optional[float] = None


@s(auto_attribs=True)
class HistoryType:
    ParcelHistoryId: Optional[int] = None
    ProcessedDate: Optional[str] = None
    ExceptionId: Optional[int] = None
    CityDepot: Optional[str] = None
    DescriptionFr: Optional[str] = None
    DescriptionEn: Optional[str] = None
    PhotoId: Optional[int] = None
    SignatureId: Optional[int] = None
    Geocoding: Optional[GeocodingType] = JStruct[GeocodingType]


@s(auto_attribs=True)
class ParcelType:
    ParcelId: Optional[int] = None
    ParcelNumber: Optional[int] = None
    ReferenceNumber: Optional[str] = None
    NCV: Optional[bool] = None
    Weight: Optional[int] = None
    Status: Optional[str] = None
    StatusDescriptionEn: Optional[str] = None
    StatusDescriptionFr: Optional[str] = None
    EstimatedDeliveryDate: Optional[str] = None
    EstimatedDeliveryTime: Optional[str] = None
    EstimatedDeliveryTimeFr: Optional[str] = None
    EstimatedDeliveryTimeEn: Optional[str] = None
    EstimatedPercentageBeforeDelivery: Optional[int] = None
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    History: List[HistoryType] = JList[HistoryType]


@s(auto_attribs=True)
class PhotoType:
    Id: Optional[int] = None
    Data: Optional[str] = None


@s(auto_attribs=True)
class StatusHistoryType:
    ShipmentStatus: Optional[str] = None
    ShipmentStatusFr: Optional[str] = None
    ShipmentStatusEn: Optional[str] = None
    StatusDate: Optional[str] = None
    LastLocation: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    CustomerId: Optional[int] = None
    ShipmentId: Optional[int] = None
    ExpeditionDate: Optional[str] = None
    TotalParcels: Optional[int] = None
    TotalWeight: Optional[float] = None
    ShipmentStatus: Optional[str] = None
    ShipmentStatusFr: Optional[str] = None
    ShipmentStatusEn: Optional[str] = None
    StatusHistories: List[StatusHistoryType] = JList[StatusHistoryType]
    ShipmentType: Optional[str] = None
    ReferenceNumber: Optional[str] = None
    Note: Optional[str] = None
    BillingAccount: Optional[int] = None
    Sender: Optional[DestinationType] = JStruct[DestinationType]
    Destination: Optional[DestinationType] = JStruct[DestinationType]
    Accessory: Optional[AccessoryType] = JStruct[AccessoryType]
    Parcels: List[ParcelType] = JList[ParcelType]
    ConsolId: Optional[int] = None
    IsInvoiced: Optional[bool] = None
    IsScanned: Optional[bool] = None
    IsConsolidated: Optional[bool] = None
    Photos: List[PhotoType] = JList[PhotoType]
