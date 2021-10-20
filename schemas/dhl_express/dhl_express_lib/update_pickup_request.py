from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Account:
    typeCode: Optional[str] = None
    number: Optional[int] = None


@s(auto_attribs=True)
class ContactInformation:
    email: Optional[str] = None
    phone: Optional[str] = None
    mobilePhone: Optional[str] = None
    companyName: Optional[str] = None
    fullName: Optional[str] = None


@s(auto_attribs=True)
class PostalAddress:
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    countryCode: Optional[str] = None
    provinceCode: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    countyName: Optional[str] = None


@s(auto_attribs=True)
class Details:
    postalAddress: Optional[PostalAddress] = JStruct[PostalAddress]
    contactInformation: Optional[ContactInformation] = JStruct[ContactInformation]


@s(auto_attribs=True)
class CustomerDetails:
    shipperDetails: Optional[Details] = JStruct[Details]
    receiverDetails: Optional[Details] = JStruct[Details]
    bookingRequestorDetails: Optional[Details] = JStruct[Details]
    pickupDetails: Optional[Details] = JStruct[Details]


@s(auto_attribs=True)
class Dimensions:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@s(auto_attribs=True)
class Package:
    typeCode: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[Dimensions] = JStruct[Dimensions]


@s(auto_attribs=True)
class ValueAddedService:
    serviceCode: Optional[str] = None
    localServiceCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    method: Optional[str] = None


@s(auto_attribs=True)
class ShipmentDetail:
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    accounts: List[Account] = JList[Account]
    valueAddedServices: List[ValueAddedService] = JList[ValueAddedService]
    isCustomsDeclarable: Optional[bool] = None
    declaredValue: Optional[int] = None
    declaredValueCurrency: Optional[str] = None
    unitOfMeasurement: Optional[str] = None
    shipmentTrackingNumber: Optional[int] = None
    packages: List[Package] = JList[Package]


@s(auto_attribs=True)
class SpecialInstruction:
    value: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class UpdatePickupRequest:
    dispatchConfirmationNumber: Optional[str] = None
    originalShipperAccountNumber: Optional[int] = None
    plannedPickupDateAndTime: Optional[str] = None
    closeTime: Optional[str] = None
    location: Optional[str] = None
    locationType: Optional[str] = None
    accounts: List[Account] = JList[Account]
    specialInstructions: List[SpecialInstruction] = JList[SpecialInstruction]
    remark: Optional[str] = None
    customerDetails: Optional[CustomerDetails] = JStruct[CustomerDetails]
    shipmentDetails: List[ShipmentDetail] = JList[ShipmentDetail]
