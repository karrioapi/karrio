from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CodAddressType:
    company: Optional[str] = None
    name: Optional[str] = None
    addressLine1: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None


@s(auto_attribs=True)
class CodType:
    codAddress: Optional[CodAddressType] = JStruct[CodAddressType]
    paymentType: Optional[str] = None


@s(auto_attribs=True)
class BillingAddressType:
    company: Optional[str] = None
    attention: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@s(auto_attribs=True)
class ContactType:
    contactCompany: Optional[str] = None
    contactName: Optional[str] = None
    phone: Optional[str] = None
    brokerName: Optional[str] = None
    brokerTaxId: Optional[str] = None
    recipientTaxId: Optional[str] = None


@s(auto_attribs=True)
class DutiesTaxesType:
    dutiable: Optional[bool] = None
    billTo: Optional[str] = None
    accountNumber: Optional[str] = None
    sedNumber: Optional[str] = None


@s(auto_attribs=True)
class ItemType:
    hsnCode: Optional[str] = None
    description: Optional[str] = None
    originCountry: Optional[str] = None
    quantity: Optional[int] = None
    unitPrice: Optional[int] = None
    skuCode: Optional[str] = None


@s(auto_attribs=True)
class ItemsType:
    item: List[ItemType] = JList[ItemType]
    currency: Optional[str] = None


@s(auto_attribs=True)
class CustomsInformationType:
    contact: Optional[ContactType] = JStruct[ContactType]
    items: Optional[ItemsType] = JStruct[ItemsType]
    dutiesTaxes: Optional[DutiesTaxesType] = JStruct[DutiesTaxesType]
    billingAddress: Optional[BillingAddressType] = JStruct[BillingAddressType]
    remarks: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    height: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    dimensionUnit: Optional[str] = None
    weight: Optional[int] = None
    weightUnit: Optional[str] = None
    type: Optional[str] = None
    freightClass: Optional[str] = None
    nmfcCode: Optional[str] = None
    insuranceAmount: Optional[int] = None
    codAmount: Optional[int] = None
    description: Optional[str] = None
    harmonizedCode: Optional[str] = None
    skuCode: Optional[str] = None


@s(auto_attribs=True)
class PackagesType:
    type: Optional[str] = None
    packages: List[PackageType] = JList[PackageType]


@s(auto_attribs=True)
class TimeType:
    hour: Optional[int] = None
    minute: Optional[int] = None
    second: Optional[int] = None
    nano: Optional[int] = None


@s(auto_attribs=True)
class PickupType:
    contactName: Optional[str] = None
    phoneNumber: Optional[str] = None
    pickupDate: Optional[str] = None
    pickupTime: Optional[TimeType] = JStruct[TimeType]
    closingTime: Optional[TimeType] = JStruct[TimeType]
    palletPickupTime: Optional[TimeType] = JStruct[TimeType]
    palletClosingTime: Optional[TimeType] = JStruct[TimeType]
    palletDeliveryClosingTime: Optional[TimeType] = JStruct[TimeType]
    location: Optional[str] = None
    instructions: Optional[str] = None


@s(auto_attribs=True)
class FromType:
    attention: Optional[str] = None
    company: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    instructions: Optional[str] = None
    residential: Optional[bool] = None
    tailgateRequired: Optional[bool] = None
    confirmDelivery: Optional[bool] = None
    notifyRecipient: Optional[bool] = None


@s(auto_attribs=True)
class ThirdPartyBillingType:
    carrier: Optional[int] = None
    country: Optional[int] = None
    billToAccountNumber: Optional[str] = None
    billToPostalCode: Optional[str] = None


@s(auto_attribs=True)
class RateRequestType:
    scheduledShipDate: Optional[str] = None
    raterequestfrom: Optional[FromType] = JStruct[FromType]
    to: Optional[FromType] = JStruct[FromType]
    packagingUnit: Optional[str] = None
    packages: Optional[PackagesType] = JStruct[PackagesType]
    reference1: Optional[str] = None
    reference2: Optional[str] = None
    reference3: Optional[str] = None
    transactionId: Optional[str] = None
    signatureRequired: Optional[str] = None
    insuranceType: Optional[str] = None
    dangerousGoodsType: Optional[str] = None
    pickup: Optional[PickupType] = JStruct[PickupType]
    customsInformation: Optional[CustomsInformationType] = JStruct[CustomsInformationType]
    customsInBondFreight: Optional[bool] = None
    cod: Optional[CodType] = JStruct[CodType]
    isSaturdayService: Optional[bool] = None
    holdForPickupRequired: Optional[bool] = None
    specialEquipment: Optional[bool] = None
    insideDelivery: Optional[bool] = None
    deliveryAppointment: Optional[bool] = None
    insidePickup: Optional[bool] = None
    saturdayPickupRequired: Optional[bool] = None
    stackable: Optional[bool] = None
    serviceId: Optional[int] = None
    thirdPartyBilling: Optional[ThirdPartyBillingType] = JStruct[ThirdPartyBillingType]
    commodityType: Optional[str] = None
