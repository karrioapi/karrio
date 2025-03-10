import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CodAddressType:
    company: typing.Optional[str] = None
    name: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None
    city: typing.Optional[str] = None
    province: typing.Optional[str] = None
    country: typing.Optional[str] = None
    zip: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CodType:
    codAddress: typing.Optional[CodAddressType] = jstruct.JStruct[CodAddressType]
    paymentType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BillingAddressType:
    company: typing.Optional[str] = None
    attention: typing.Optional[str] = None
    address1: typing.Optional[str] = None
    address2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    province: typing.Optional[str] = None
    country: typing.Optional[str] = None
    zip: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactType:
    contactCompany: typing.Optional[str] = None
    contactName: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    brokerName: typing.Optional[str] = None
    brokerTaxId: typing.Optional[str] = None
    recipientTaxId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DutiesTaxesType:
    dutiable: typing.Optional[bool] = None
    billTo: typing.Optional[str] = None
    accountNumber: typing.Optional[str] = None
    sedNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemType:
    hsnCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    originCountry: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    unitPrice: typing.Optional[int] = None
    skuCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemsType:
    item: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsInformationType:
    contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]
    items: typing.Optional[ItemsType] = jstruct.JStruct[ItemsType]
    dutiesTaxes: typing.Optional[DutiesTaxesType] = jstruct.JStruct[DutiesTaxesType]
    billingAddress: typing.Optional[BillingAddressType] = jstruct.JStruct[BillingAddressType]
    remarks: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    height: typing.Optional[int] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    dimensionUnit: typing.Optional[str] = None
    weight: typing.Optional[int] = None
    weightUnit: typing.Optional[str] = None
    type: typing.Optional[str] = None
    freightClass: typing.Optional[str] = None
    nmfcCode: typing.Optional[str] = None
    insuranceAmount: typing.Optional[int] = None
    codAmount: typing.Optional[int] = None
    description: typing.Optional[str] = None
    harmonizedCode: typing.Optional[str] = None
    skuCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackagesType:
    type: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    weightUnit: typing.Optional[str] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    totalWeight: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class TimeType:
    hour: typing.Optional[int] = None
    minute: typing.Optional[int] = None
    second: typing.Optional[int] = None
    nano: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupType:
    contactName: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    pickupDate: typing.Optional[str] = None
    pickupTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    closingTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    palletPickupTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    palletClosingTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    palletDeliveryClosingTime: typing.Optional[TimeType] = jstruct.JStruct[TimeType]
    location: typing.Optional[str] = None
    instructions: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FromType:
    attention: typing.Optional[str] = None
    company: typing.Optional[str] = None
    address1: typing.Optional[str] = None
    address2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    province: typing.Optional[str] = None
    country: typing.Optional[str] = None
    zip: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    instructions: typing.Optional[str] = None
    residential: typing.Optional[bool] = None
    tailgateRequired: typing.Optional[bool] = None
    confirmDelivery: typing.Optional[bool] = None
    notifyRecipient: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ThirdPartyBillingType:
    carrier: typing.Optional[int] = None
    country: typing.Optional[int] = None
    billToAccountNumber: typing.Optional[str] = None
    billToPostalCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRequestType:
    scheduledShipDate: typing.Optional[str] = None
    shippingrequestfrom: typing.Optional[FromType] = jstruct.JStruct[FromType]
    to: typing.Optional[FromType] = jstruct.JStruct[FromType]
    packagingUnit: typing.Optional[str] = None
    packages: typing.Optional[PackagesType] = jstruct.JStruct[PackagesType]
    reference1: typing.Optional[str] = None
    reference2: typing.Optional[str] = None
    reference3: typing.Optional[str] = None
    transactionId: typing.Optional[str] = None
    billingReference: typing.Optional[str] = None
    signatureRequired: typing.Optional[str] = None
    insuranceType: typing.Optional[str] = None
    dangerousGoodsType: typing.Optional[str] = None
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
    customsInformation: typing.Optional[CustomsInformationType] = jstruct.JStruct[CustomsInformationType]
    thirdPartyBilling: typing.Optional[ThirdPartyBillingType] = jstruct.JStruct[ThirdPartyBillingType]
    commodityType: typing.Optional[str] = None
    isSaturdayService: typing.Optional[bool] = None
    holdForPickupRequired: typing.Optional[bool] = None
    specialEquipment: typing.Optional[bool] = None
    deliveryAppointment: typing.Optional[bool] = None
    insideDelivery: typing.Optional[bool] = None
    insidePickup: typing.Optional[bool] = None
    saturdayPickupRequired: typing.Optional[bool] = None
    stackable: typing.Optional[bool] = None
    serviceId: typing.Optional[int] = None
    cod: typing.Optional[CodType] = jstruct.JStruct[CodType]
