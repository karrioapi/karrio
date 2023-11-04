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
class DimensionsType:
    Height: Optional[float] = None
    Length: Optional[float] = None
    Width: Optional[float] = None
    Cubing: Optional[float] = None


@s(auto_attribs=True)
class ParcelType:
    NCV: Optional[bool] = None
    Weight: Optional[float] = None
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]


@s(auto_attribs=True)
class RateRequestType:
    CustomerId: Optional[int] = None
    ExpeditionDate: Optional[str] = None
    ShipmentType: Optional[str] = None
    SourcePostalCode: Optional[str] = None
    DestinationPostalCode: Optional[str] = None
    TotalWeight: Optional[float] = None
    TotalParcels: Optional[int] = None
    UnitsOfMeasurement: Optional[str] = None
    Accessory: Optional[AccessoryType] = JStruct[AccessoryType]
    Parcels: List[ParcelType] = JList[ParcelType]
