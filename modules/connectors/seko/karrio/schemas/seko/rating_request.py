import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressType:
    BuildingName: typing.Optional[str] = None
    StreetAddress: typing.Optional[str] = None
    Suburb: typing.Optional[str] = None
    City: typing.Optional[str] = None
    PostCode: typing.Optional[int] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DestinationType:
    Id: typing.Optional[int] = None
    Name: typing.Optional[str] = None
    Address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    ContactPerson: typing.Optional[str] = None
    PhoneNumber: typing.Optional[int] = None
    Email: typing.Optional[str] = None
    DeliveryInstructions: typing.Optional[str] = None
    RecipientTaxId: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackageType:
    Height: typing.Optional[int] = None
    Length: typing.Optional[int] = None
    Id: typing.Optional[int] = None
    Width: typing.Optional[int] = None
    Kg: typing.Optional[float] = None
    Name: typing.Optional[str] = None
    PackageCode: typing.Optional[str] = None
    Type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RatingRequestType:
    DeliveryReference: typing.Optional[str] = None
    Destination: typing.Optional[DestinationType] = jstruct.JStruct[DestinationType]
    IsSaturdayDelivery: typing.Optional[bool] = None
    IsSignatureRequired: typing.Optional[bool] = None
    Packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
