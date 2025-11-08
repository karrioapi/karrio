import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ContactInformationType:
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    mobilePhone: typing.Optional[str] = None
    companyName: typing.Optional[str] = None
    fullName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PostalAddressType:
    postalCode: typing.Optional[int] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipperDetailsType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[ShipperDetailsType] = jstruct.JStruct[ShipperDetailsType]


@attr.s(auto_attribs=True)
class SpecialInstructionType:
    value: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupUpdateRequestType:
    plannedPickupDateAndTime: typing.Optional[str] = None
    closeTime: typing.Optional[str] = None
    location: typing.Optional[str] = None
    locationType: typing.Optional[str] = None
    specialInstructions: typing.Optional[typing.List[SpecialInstructionType]] = jstruct.JList[SpecialInstructionType]
    remark: typing.Optional[str] = None
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
