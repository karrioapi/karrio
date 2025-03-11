import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DropoffType:
    ContactName: typing.Optional[str] = None
    Email: typing.Optional[str] = None
    Phone: typing.Optional[str] = None
    UnitNumber: typing.Optional[str] = None
    StreetNumber: typing.Optional[int] = None
    Street: typing.Optional[str] = None
    Suburb: typing.Optional[str] = None
    State: typing.Optional[str] = None
    Postcode: typing.Optional[int] = None
    Country: typing.Optional[str] = None
    Notes: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRequestType:
    PurchaseOrderNumber: typing.Optional[str] = None
    PackageDescription: typing.Optional[str] = None
    DeliverySpeed: typing.Optional[str] = None
    ReadyDateTime: typing.Optional[str] = None
    VehicleType: typing.Optional[str] = None
    PackageType: typing.Optional[str] = None
    Pickup: typing.Optional[DropoffType] = jstruct.JStruct[DropoffType]
    Dropoff: typing.Optional[DropoffType] = jstruct.JStruct[DropoffType]
