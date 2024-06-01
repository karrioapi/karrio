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
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    countryCode: Optional[str] = None
    provinceCode: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    countyName: Optional[str] = None


@s(auto_attribs=True)
class DetailsType:
    postalAddress: Optional[PostalAddressType] = JStruct[PostalAddressType]
    contactInformation: Optional[ContactInformationType] = JStruct[ContactInformationType]


@s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: Optional[DetailsType] = JStruct[DetailsType]
    receiverDetails: Optional[DetailsType] = JStruct[DetailsType]
    bookingRequestorDetails: Optional[DetailsType] = JStruct[DetailsType]
    pickupDetails: Optional[DetailsType] = JStruct[DetailsType]


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
    localServiceCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    method: Optional[str] = None


@s(auto_attribs=True)
class ShipmentDetailType:
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    accounts: List[AccountType] = JList[AccountType]
    valueAddedServices: List[ValueAddedServiceType] = JList[ValueAddedServiceType]
    isCustomsDeclarable: Optional[bool] = None
    declaredValue: Optional[int] = None
    declaredValueCurrency: Optional[str] = None
    unitOfMeasurement: Optional[str] = None
    shipmentTrackingNumber: Optional[int] = None
    packages: List[PackageType] = JList[PackageType]


@s(auto_attribs=True)
class SpecialInstructionType:
    value: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class PickupUpdateType:
    dispatchConfirmationNumber: Optional[str] = None
    originalShipperAccountNumber: Optional[int] = None
    plannedPickupDateAndTime: Optional[str] = None
    closeTime: Optional[str] = None
    location: Optional[str] = None
    locationType: Optional[str] = None
    accounts: List[AccountType] = JList[AccountType]
    specialInstructions: List[SpecialInstructionType] = JList[SpecialInstructionType]
    remark: Optional[str] = None
    customerDetails: Optional[CustomerDetailsType] = JStruct[CustomerDetailsType]
    shipmentDetails: List[ShipmentDetailType] = JList[ShipmentDetailType]
