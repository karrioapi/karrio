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
class DimensionsType:
    Height: typing.Optional[float] = None
    Length: typing.Optional[float] = None
    Width: typing.Optional[float] = None
    Cubing: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ParcelType:
    NCV: typing.Optional[bool] = None
    Weight: typing.Optional[float] = None
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class RateRequestType:
    CustomerId: typing.Optional[int] = None
    ExpeditionDate: typing.Optional[str] = None
    ShipmentType: typing.Optional[str] = None
    SourcePostalCode: typing.Optional[str] = None
    DestinationPostalCode: typing.Optional[str] = None
    TotalWeight: typing.Optional[float] = None
    TotalParcels: typing.Optional[int] = None
    UnitsOfMeasurement: typing.Optional[str] = None
    Accessory: typing.Optional[AccessoryType] = jstruct.JStruct[AccessoryType]
    Parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
