from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Cod:
    CODType: Optional[str] = None
    CODAmount: Optional[float] = None


@s(auto_attribs=True)
class Accessory:
    InsuranceAmount: Optional[int] = None
    FrozenProtection: Optional[bool] = None
    DangerousGoods: Optional[bool] = None
    Before10h30am: Optional[bool] = None
    SNR: Optional[bool] = None
    COD: Optional[Cod] = JStruct[Cod]


@s(auto_attribs=True)
class Destination:
    Contact: Optional[str] = None
    AccountNumber: Optional[str] = None
    AccountName: Optional[str] = None
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    PostalCode: Optional[str] = None
    City: Optional[str] = None
    ProvinceState: Optional[str] = None
    Phone: Optional[int] = None
    SmsNotification: Optional[bool] = None
    EmailNotification: Optional[bool] = None
    NoCivic: Optional[int] = None
    Suite: Optional[int] = None
    StreetName: Optional[str] = None
    Email: Optional[str] = None


@s(auto_attribs=True)
class Dimensions:
    Height: Optional[float] = None
    Length: Optional[int] = None
    Width: Optional[int] = None
    Cubing: Optional[float] = None


@s(auto_attribs=True)
class Geocoding:
    Longitude: Optional[float] = None
    Latitude: Optional[float] = None


@s(auto_attribs=True)
class History:
    ParcelHistoryId: Optional[int] = None
    ProcessedDate: Optional[str] = None
    ExceptionId: Optional[int] = None
    CityDepot: Optional[str] = None
    DescriptionFr: Optional[str] = None
    DescriptionEn: Optional[str] = None
    PhotoId: Optional[int] = None
    SignatureId: Optional[int] = None
    Geocoding: Optional[Geocoding] = JStruct[Geocoding]


@s(auto_attribs=True)
class Parcel:
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
    Dimensions: Optional[Dimensions] = JStruct[Dimensions]
    History: List[History] = JList[History]


@s(auto_attribs=True)
class Photo:
    Id: Optional[int] = None
    Data: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponse:
    CustomerId: Optional[int] = None
    ShipmentId: Optional[int] = None
    ExpeditionDate: Optional[str] = None
    TotalParcels: Optional[int] = None
    TotalWeight: Optional[float] = None
    ShipmentStatus: Optional[str] = None
    ShipmentStatusFr: Optional[str] = None
    ShipmentStatusEn: Optional[str] = None
    ShipmentType: Optional[str] = None
    ReferenceNumber: Optional[str] = None
    Note: Optional[str] = None
    BillingAccount: Optional[int] = None
    Sender: Optional[Destination] = JStruct[Destination]
    Destination: Optional[Destination] = JStruct[Destination]
    Accessory: Optional[Accessory] = JStruct[Accessory]
    Parcels: List[Parcel] = JList[Parcel]
    ConsolId: Optional[int] = None
    Photos: List[Photo] = JList[Photo]
