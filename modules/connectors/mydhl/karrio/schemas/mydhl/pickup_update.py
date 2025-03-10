import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[int] = None


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
    provinceCode: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    countyName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DetailsType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    receiverDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    bookingRequestorDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]
    pickupDetails: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]


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
class ValueAddedServiceType:
    serviceCode: typing.Optional[str] = None
    localServiceCode: typing.Optional[str] = None
    value: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    method: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentDetailType:
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    valueAddedServices: typing.Optional[typing.List[ValueAddedServiceType]] = jstruct.JList[ValueAddedServiceType]
    isCustomsDeclarable: typing.Optional[bool] = None
    declaredValue: typing.Optional[int] = None
    declaredValueCurrency: typing.Optional[str] = None
    unitOfMeasurement: typing.Optional[str] = None
    shipmentTrackingNumber: typing.Optional[int] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]


@attr.s(auto_attribs=True)
class SpecialInstructionType:
    value: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupUpdateType:
    dispatchConfirmationNumber: typing.Optional[str] = None
    originalShipperAccountNumber: typing.Optional[int] = None
    plannedPickupDateAndTime: typing.Optional[str] = None
    closeTime: typing.Optional[str] = None
    location: typing.Optional[str] = None
    locationType: typing.Optional[str] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    specialInstructions: typing.Optional[typing.List[SpecialInstructionType]] = jstruct.JList[SpecialInstructionType]
    remark: typing.Optional[str] = None
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    shipmentDetails: typing.Optional[typing.List[ShipmentDetailType]] = jstruct.JList[ShipmentDetailType]
