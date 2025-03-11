import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccessoryType:
    InsuranceAmount: typing.Optional[float] = None
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
class ParcelType:
    NCV: typing.Optional[bool] = None
    Weight: typing.Optional[float] = None
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    CustomerId: typing.Optional[int] = None
    ShipmentId: typing.Optional[int] = None
    ExpeditionDate: typing.Optional[str] = None
    ShipmentType: typing.Optional[str] = None
    TotalParcels: typing.Optional[int] = None
    TotalWeight: typing.Optional[float] = None
    ReferenceNumber: typing.Optional[str] = None
    CustomBarcode: typing.Optional[str] = None
    Note: typing.Optional[str] = None
    BillingAccount: typing.Optional[int] = None
    Sender: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    Destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    Accessory: typing.Optional[AccessoryType] = jstruct.JStruct[AccessoryType]
    Parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    UnitsOfMeasurement: typing.Optional[str] = None
