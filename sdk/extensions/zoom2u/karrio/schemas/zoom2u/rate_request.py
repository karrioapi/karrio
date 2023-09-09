from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class DropoffType:
    ContactName: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    UnitNumber: Optional[str] = None
    StreetNumber: Optional[int] = None
    Street: Optional[str] = None
    Suburb: Optional[str] = None
    State: Optional[str] = None
    Postcode: Optional[int] = None
    Country: Optional[str] = None
    Notes: Optional[str] = None


@s(auto_attribs=True)
class RateRequestType:
    PurchaseOrderNumber: Optional[str] = None
    PackageDescription: Optional[str] = None
    DeliverySpeed: Optional[str] = None
    ReadyDateTime: Optional[str] = None
    VehicleType: Optional[str] = None
    PackageType: Optional[str] = None
    Pickup: Optional[DropoffType] = JStruct[DropoffType]
    Dropoff: Optional[DropoffType] = JStruct[DropoffType]
