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
class Dimensions:
    Height: Optional[float] = None
    Length: Optional[int] = None
    Width: Optional[int] = None
    Cubing: Optional[float] = None


@s(auto_attribs=True)
class Parcel:
    NCV: Optional[bool] = None
    Weight: Optional[float] = None
    Dimensions: Optional[Dimensions] = JStruct[Dimensions]


@s(auto_attribs=True)
class RateRequest:
    CustomerId: Optional[int] = None
    ExpeditionDate: Optional[str] = None
    ShipmentType: Optional[str] = None
    SourcePostalCode: Optional[str] = None
    DestinationPostalCode: Optional[str] = None
    TotalWeight: Optional[float] = None
    TotalParcels: Optional[int] = None
    UnitsOfMeasurement: Optional[str] = None
    Accessory: Optional[Accessory] = JStruct[Accessory]
    Parcels: List[Parcel] = JList[Parcel]
