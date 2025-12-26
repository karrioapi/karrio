import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class FiscalRepresentationAddressType:
    company: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    town: typing.Optional[str] = None
    addressAddition: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    mobile: typing.Optional[str] = None
    mail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ClientType:
    eoriNumber: typing.Optional[str] = None
    iossId: typing.Optional[str] = None
    vatId: typing.Optional[str] = None
    zazAccount: typing.Optional[str] = None
    fiscalRepresentationAddress: typing.Optional[FiscalRepresentationAddressType] = jstruct.JStruct[FiscalRepresentationAddressType]


@attr.s(auto_attribs=True)
class ItemType:
    sku: typing.Optional[str] = None
    category: typing.Optional[str] = None
    countryCodeOfManufacture: typing.Optional[str] = None
    value: typing.Optional[int] = None
    weight: typing.Optional[int] = None
    quantity: typing.Optional[int] = None
    description: typing.Optional[str] = None
    exportDescription: typing.Optional[str] = None
    exportHsCode: typing.Optional[str] = None
    hsCode: typing.Optional[str] = None
    url: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentOriginAddressType:
    title: typing.Optional[str] = None
    firstname: typing.Optional[str] = None
    lastname: typing.Optional[str] = None
    company: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    town: typing.Optional[str] = None
    state: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    addressAddition: typing.Optional[str] = None
    addressAddition2: typing.Optional[str] = None
    addressAddition3: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    fax: typing.Optional[str] = None
    mobile: typing.Optional[str] = None
    mail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsAndTaxesType:
    currency: typing.Optional[str] = None
    shipmentCost: typing.Optional[int] = None
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    invoiceReferences: typing.Optional[typing.List[str]] = None
    value: typing.Optional[int] = None
    exportCustomsClearance: typing.Optional[bool] = None
    client: typing.Optional[ClientType] = jstruct.JStruct[ClientType]
    shipmentOriginAddress: typing.Optional[ShipmentOriginAddressType] = jstruct.JStruct[ShipmentOriginAddressType]


@attr.s(auto_attribs=True)
class ParcelType:
    parcelClass: typing.Optional[str] = None
    parcelHeight: typing.Optional[int] = None
    parcelWidth: typing.Optional[int] = None
    parcelDepth: typing.Optional[int] = None
    parcelWeight: typing.Optional[int] = None
    parcelVolume: typing.Optional[int] = None
    productType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErAddressType:
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    town: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    addressAddition: typing.Optional[str] = None
    addressAddition2: typing.Optional[str] = None
    addressAddition3: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverContactType:
    phone: typing.Optional[str] = None
    mobile: typing.Optional[str] = None
    mail: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErNameType:
    title: typing.Optional[str] = None
    gender: typing.Optional[str] = None
    firstname: typing.Optional[str] = None
    middlename: typing.Optional[str] = None
    lastname: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CashOnDeliveryServiceType:
    currency: typing.Optional[str] = None
    amount: typing.Optional[float] = None
    bankTransferAmount: typing.Optional[float] = None
    bankTransferCurrency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerAlertServiceType:
    notificationType: typing.Optional[str] = None
    notificationEmail: typing.Optional[str] = None
    notificationNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IdentServiceType:
    identID: typing.Optional[str] = None
    identType: typing.Optional[str] = None
    identVerifyFsk: typing.Optional[str] = None
    identVerifyBirthday: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MultipartServiceType:
    partNumber: typing.Optional[int] = None
    numberOfParts: typing.Optional[int] = None
    parentShipmentOrderID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelShopDeliveryServiceType:
    psCustomerFirstName: typing.Optional[str] = None
    psCustomerLastName: typing.Optional[str] = None
    psID: typing.Optional[str] = None
    psSelectionRule: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatedDayServiceType:
    statedDay: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class StatedTimeServiceType:
    timeSlot: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceType:
    tanService: typing.Optional[bool] = None
    multipartService: typing.Optional[MultipartServiceType] = jstruct.JStruct[MultipartServiceType]
    limitedQuantitiesService: typing.Optional[bool] = None
    cashOnDeliveryService: typing.Optional[CashOnDeliveryServiceType] = jstruct.JStruct[CashOnDeliveryServiceType]
    bulkGoodService: typing.Optional[bool] = None
    statedTimeService: typing.Optional[StatedTimeServiceType] = jstruct.JStruct[StatedTimeServiceType]
    householdSignatureService: typing.Optional[bool] = None
    customerAlertService: typing.Optional[CustomerAlertServiceType] = jstruct.JStruct[CustomerAlertServiceType]
    parcelShopDeliveryService: typing.Optional[ParcelShopDeliveryServiceType] = jstruct.JStruct[ParcelShopDeliveryServiceType]
    compactParcelService: typing.Optional[bool] = None
    identService: typing.Optional[IdentServiceType] = jstruct.JStruct[IdentServiceType]
    statedDayService: typing.Optional[StatedDayServiceType] = jstruct.JStruct[StatedDayServiceType]
    nextDayService: typing.Optional[bool] = None
    signatureService: typing.Optional[bool] = None
    redirectionProhibitedService: typing.Optional[bool] = None
    excludeParcelShopAuthorization: typing.Optional[bool] = None
    lateInjectionService: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    clientReference: typing.Optional[str] = None
    clientReference2: typing.Optional[str] = None
    receiverName: typing.Optional[ErNameType] = jstruct.JStruct[ErNameType]
    receiverAddress: typing.Optional[ErAddressType] = jstruct.JStruct[ErAddressType]
    receiverContact: typing.Optional[ReceiverContactType] = jstruct.JStruct[ReceiverContactType]
    senderName: typing.Optional[ErNameType] = jstruct.JStruct[ErNameType]
    senderAddress: typing.Optional[ErAddressType] = jstruct.JStruct[ErAddressType]
    parcel: typing.Optional[ParcelType] = jstruct.JStruct[ParcelType]
    service: typing.Optional[ServiceType] = jstruct.JStruct[ServiceType]
    customsAndTaxes: typing.Optional[CustomsAndTaxesType] = jstruct.JStruct[CustomsAndTaxesType]
