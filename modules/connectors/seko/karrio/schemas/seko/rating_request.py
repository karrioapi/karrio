from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AddressType:
    BuildingName: Optional[str] = None
    StreetAddress: Optional[str] = None
    Suburb: Optional[str] = None
    City: Optional[str] = None
    PostCode: Optional[int] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class DestinationType:
    Id: Optional[int] = None
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    ContactPerson: Optional[str] = None
    PhoneNumber: Optional[int] = None
    Email: Optional[str] = None
    DeliveryInstructions: Optional[str] = None
    RecipientTaxId: Optional[int] = None


@s(auto_attribs=True)
class PackageType:
    Height: Optional[int] = None
    Length: Optional[int] = None
    Id: Optional[int] = None
    Width: Optional[int] = None
    Kg: Optional[float] = None
    Name: Optional[str] = None
    PackageCode: Optional[str] = None
    Type: Optional[str] = None


@s(auto_attribs=True)
class RatingRequestType:
    DeliveryReference: Optional[str] = None
    Destination: Optional[DestinationType] = JStruct[DestinationType]
    IsSaturdayDelivery: Optional[bool] = None
    IsSignatureRequired: Optional[bool] = None
    Packages: List[PackageType] = JList[PackageType]
