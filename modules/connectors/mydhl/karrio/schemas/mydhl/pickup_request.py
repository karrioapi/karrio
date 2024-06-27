from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccountType:
    typeCode: Optional[str] = None
    number: Optional[int] = None


@s(auto_attribs=True)
class ContactInformationType:
    email: Optional[str] = None
    phone: Optional[str] = None
    mobilePhone: Optional[str] = None
    companyName: Optional[str] = None
    fullName: Optional[str] = None


@s(auto_attribs=True)
class PostalAddressType:
    postalCode: Optional[str] = None
    cityName: Optional[str] = None
    countryCode: Optional[str] = None
    provinceCode: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    countyName: Optional[str] = None


@s(auto_attribs=True)
class ErDetailsType:
    postalAddress: Optional[PostalAddressType] = JStruct[PostalAddressType]
    contactInformation: Optional[ContactInformationType] = JStruct[ContactInformationType]


@s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: Optional[ErDetailsType] = JStruct[ErDetailsType]
    receiverDetails: Optional[ErDetailsType] = JStruct[ErDetailsType]


@s(auto_attribs=True)
class DimensionsType:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@s(auto_attribs=True)
class PackageType:
    typeCode: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]


@s(auto_attribs=True)
class ValueAddedServiceType:
    serviceCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class ShipmentDetailType:
    accounts: List[AccountType] = JList[AccountType]
    packages: List[PackageType] = JList[PackageType]
    productCode: Optional[str] = None
    declaredValue: Optional[int] = None
    unitOfMeasurement: Optional[str] = None
    valueAddedServices: List[ValueAddedServiceType] = JList[ValueAddedServiceType]
    isCustomsDeclarable: Optional[bool] = None
    declaredValueCurrency: Optional[str] = None


@s(auto_attribs=True)
class SpecialInstructionType:
    value: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class PickupRequestType:
    plannedPickupDateAndTime: Optional[str] = None
    closeTime: Optional[str] = None
    location: Optional[str] = None
    locationType: Optional[str] = None
    accounts: List[AccountType] = JList[AccountType]
    specialInstructions: List[SpecialInstructionType] = JList[SpecialInstructionType]
    remark: Optional[str] = None
    customerDetails: Optional[CustomerDetailsType] = JStruct[CustomerDetailsType]
    shipmentDetails: List[ShipmentDetailType] = JList[ShipmentDetailType]
