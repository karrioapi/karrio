import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccessoryType:
    InsuranceAmount: typing.Optional[int] = None
    FrozenProtection: typing.Optional[bool] = None
    DangerousGoods: typing.Optional[bool] = None
    SNR: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class DestinationType:
    Contact: typing.Optional[str] = None
    AccountNumber: typing.Optional[str] = None
    AccountName: typing.Optional[str] = None
    Address1: typing.Optional[str] = None
    Address2: typing.Optional[str] = None
    PostalCode: typing.Optional[str] = None
    City: typing.Optional[str] = None
    ProvinceState: typing.Optional[str] = None
    Phone: typing.Optional[str] = None
    SmsNotification: typing.Optional[bool] = None
    EmailNotification: typing.Optional[bool] = None
    NoCivic: typing.Optional[int] = None
    Suite: typing.Optional[int] = None
    StreetName: typing.Optional[str] = None
    Email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    Height: typing.Optional[float] = None
    Length: typing.Optional[int] = None
    Width: typing.Optional[int] = None
    Cubing: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class GeocodingType:
    Longitude: typing.Optional[float] = None
    Latitude: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class HistoryType:
    ParcelHistoryId: typing.Optional[int] = None
    ProcessedDate: typing.Optional[str] = None
    ExceptionId: typing.Optional[int] = None
    CityDepot: typing.Optional[str] = None
    DescriptionFr: typing.Optional[str] = None
    DescriptionEn: typing.Optional[str] = None
    PhotoId: typing.Optional[int] = None
    SignatureId: typing.Optional[int] = None
    Geocoding: typing.Optional[GeocodingType] = jstruct.JStruct[GeocodingType]


@attr.s(auto_attribs=True)
class ParcelType:
    ParcelId: typing.Optional[int] = None
    ParcelNumber: typing.Optional[int] = None
    ReferenceNumber: typing.Optional[str] = None
    NCV: typing.Optional[bool] = None
    Weight: typing.Optional[int] = None
    Status: typing.Optional[str] = None
    StatusDescriptionEn: typing.Optional[str] = None
    StatusDescriptionFr: typing.Optional[str] = None
    EstimatedDeliveryDate: typing.Optional[str] = None
    EstimatedDeliveryTime: typing.Optional[str] = None
    EstimatedDeliveryTimeFr: typing.Optional[str] = None
    EstimatedDeliveryTimeEn: typing.Optional[str] = None
    EstimatedPercentageBeforeDelivery: typing.Optional[int] = None
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    History: typing.Optional[typing.List[HistoryType]] = jstruct.JList[HistoryType]


@attr.s(auto_attribs=True)
class PhotoType:
    Id: typing.Optional[int] = None
    Data: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatusHistoryType:
    ShipmentStatus: typing.Optional[str] = None
    ShipmentStatusFr: typing.Optional[str] = None
    ShipmentStatusEn: typing.Optional[str] = None
    StatusDate: typing.Optional[str] = None
    LastLocation: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    CustomerId: typing.Optional[int] = None
    ShipmentId: typing.Optional[int] = None
    ExpeditionDate: typing.Optional[str] = None
    TotalParcels: typing.Optional[int] = None
    TotalWeight: typing.Optional[float] = None
    ShipmentStatus: typing.Optional[str] = None
    ShipmentStatusFr: typing.Optional[str] = None
    ShipmentStatusEn: typing.Optional[str] = None
    StatusHistories: typing.Optional[typing.List[StatusHistoryType]] = jstruct.JList[StatusHistoryType]
    ShipmentType: typing.Optional[str] = None
    ReferenceNumber: typing.Optional[str] = None
    Note: typing.Optional[str] = None
    BillingAccount: typing.Optional[int] = None
    Sender: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    Destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    Accessory: typing.Optional[AccessoryType] = jstruct.JStruct[AccessoryType]
    Parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    ConsolId: typing.Optional[int] = None
    IsInvoiced: typing.Optional[bool] = None
    IsScanned: typing.Optional[bool] = None
    IsConsolidated: typing.Optional[bool] = None
    Photos: typing.Optional[typing.List[PhotoType]] = jstruct.JList[PhotoType]
