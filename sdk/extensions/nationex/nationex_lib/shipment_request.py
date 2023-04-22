from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccessoryType:
    InsuranceAmount: Optional[float] = None
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
class ParcelType:
    NCV: Optional[bool] = None
    Weight: Optional[float] = None
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]


@s(auto_attribs=True)
class ShipmentRequestType:
    CustomerId: Optional[int] = None
    ShipmentId: Optional[int] = None
    ExpeditionDate: Optional[str] = None
    ShipmentType: Optional[str] = None
    TotalParcels: Optional[int] = None
    TotalWeight: Optional[float] = None
    ReferenceNumber: Optional[str] = None
    CustomBarcode: Optional[str] = None
    Note: Optional[str] = None
    BillingAccount: Optional[int] = None
    Sender: Optional[DestinationType] = JStruct[DestinationType]
    Destination: Optional[DestinationType] = JStruct[DestinationType]
    Accessory: Optional[AccessoryType] = JStruct[AccessoryType]
    Parcels: List[ParcelType] = JList[ParcelType]
    UnitsOfMeasurement: Optional[str] = None
