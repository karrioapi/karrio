import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactInformationType:
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    mobilePhone: typing.Optional[str] = None
    companyName: typing.Optional[str] = None
    fullName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PostalAddressType:
    postalCode: typing.Optional[str] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErDetailsType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[ErDetailsType] = jstruct.JStruct[ErDetailsType]
    receiverDetails: typing.Optional[ErDetailsType] = jstruct.JStruct[ErDetailsType]


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackageType:
    typeCode: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ShipmentDetailType:
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    isCustomsDeclarable: typing.Optional[bool] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SpecialInstructionType:
    value: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupCreateRequestType:
    plannedPickupDateAndTime: typing.Optional[str] = None
    closeTime: typing.Optional[str] = None
    location: typing.Optional[str] = None
    locationType: typing.Optional[str] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    specialInstructions: typing.Optional[typing.List[SpecialInstructionType]] = jstruct.JList[SpecialInstructionType]
    remark: typing.Optional[str] = None
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    shipmentDetails: typing.Optional[typing.List[ShipmentDetailType]] = jstruct.JList[ShipmentDetailType]
