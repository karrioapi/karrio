import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DeliveryType:
    dateFrom: typing.Optional[str] = None
    dateTo: typing.Optional[str] = None
    timeFrom: typing.Optional[str] = None
    timeTo: typing.Optional[str] = None
    timeSlotTariff: typing.Any = None


@attr.s(auto_attribs=True)
class CustomsAmountType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExporterAddressType:
    companyName: typing.Optional[str] = None
    name1: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExporterContactType:
    phone1: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExporterType:
    address: typing.Optional[ExporterAddressType] = jstruct.JStruct[ExporterAddressType]
    contact: typing.Optional[ExporterContactType] = jstruct.JStruct[ExporterContactType]
    eori: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ImporterType:
    address: typing.Optional[ExporterAddressType] = jstruct.JStruct[ExporterAddressType]
    contact: typing.Optional[ExporterContactType] = jstruct.JStruct[ExporterContactType]
    gln: typing.Any = None
    vatNumber: typing.Optional[str] = None
    customerDefermentNumber: typing.Any = None
    eori: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InterInvoiceLineType:
    invoicePosition: typing.Optional[str] = None
    quantityOfItems: typing.Optional[str] = None
    content: typing.Optional[str] = None
    amountOfPosition: typing.Optional[float] = None
    manufacturedCountry: typing.Optional[str] = None
    netWeight: typing.Optional[str] = None
    grossWeight: typing.Optional[str] = None
    customerProductCode: typing.Optional[str] = None
    productDescription: typing.Optional[str] = None
    fabricComposition: typing.Any = None
    importTarifCode: typing.Optional[str] = None
    exportTarifCode: typing.Optional[str] = None
    goodsWebPage: typing.Any = None
    parcelRank: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalType:
    parcelType: typing.Optional[str] = None
    customsAmount: typing.Optional[CustomsAmountType] = jstruct.JStruct[CustomsAmountType]
    customsAmountEx: typing.Optional[CustomsAmountType] = jstruct.JStruct[CustomsAmountType]
    customsTerms: typing.Optional[str] = None
    customsPaper: typing.Optional[str] = None
    clearanceStatus: typing.Optional[str] = None
    customsHighLowValue: typing.Optional[str] = None
    customsInvoice: typing.Optional[str] = None
    customsInvoiceDates: typing.Optional[typing.List[str]] = None
    mrn: typing.Any = None
    numberOfArticles: typing.Optional[str] = None
    destinationCountryRegistration: typing.Any = None
    exportReason: typing.Optional[str] = None
    shipmentContent: typing.Optional[str] = None
    importer: typing.Optional[ImporterType] = jstruct.JStruct[ImporterType]
    exporter: typing.Optional[ExporterType] = jstruct.JStruct[ExporterType]
    interInvoiceLines: typing.Optional[typing.List[InterInvoiceLineType]] = jstruct.JList[InterInvoiceLineType]


@attr.s(auto_attribs=True)
class CodType:
    amount: typing.Optional[CustomsAmountType] = jstruct.JStruct[CustomsAmountType]
    collectType: typing.Optional[str] = None
    purpose: typing.Any = None
    bankCode: typing.Any = None
    bankName: typing.Any = None
    bankAccountNumber: typing.Any = None
    bankAccountName: typing.Any = None
    iban: typing.Any = None
    bic: typing.Any = None


@attr.s(auto_attribs=True)
class HazardousType:
    classCode: typing.Any = None
    identificationClass: typing.Any = None
    substanceWeight: typing.Any = None
    factor: typing.Any = None
    notOtherwiseSpecified: typing.Any = None
    packingGroup: typing.Any = None
    subsidiaryRisk: typing.Any = None
    description: typing.Any = None
    hazardousWeight: typing.Any = None
    tunnelRestrictionCode: typing.Any = None
    identificationUnNo: typing.Any = None
    packingCode: typing.Any = None


@attr.s(auto_attribs=True)
class InsuranceType:
    insuranceAmount: typing.Optional[CustomsAmountType] = jstruct.JStruct[CustomsAmountType]
    insuranceParcelContent: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Email1Type:
    notificationType: typing.Optional[str] = None
    notificationEmail: typing.Optional[str] = None
    notificationLanguage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Sms1Type:
    notificationType: typing.Optional[str] = None
    notificationPhone: typing.Optional[str] = None
    notificationLanguage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MessagesType:
    email1: typing.Optional[Email1Type] = jstruct.JStruct[Email1Type]
    sms1: typing.Optional[Sms1Type] = jstruct.JStruct[Sms1Type]


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ParcelInfosType:
    weight: typing.Optional[str] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class PersonType:
    personToNotify: typing.Optional[str] = None
    personToDeliver: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReferenceType:
    referenceNumber: typing.Optional[str] = None
    referenceType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    parcelInfos: typing.Optional[ParcelInfosType] = jstruct.JStruct[ParcelInfosType]
    parcelContent: typing.Optional[str] = None
    references: typing.Optional[typing.List[ReferenceType]] = jstruct.JList[ReferenceType]
    hazardous: typing.Optional[HazardousType] = jstruct.JStruct[HazardousType]
    cod: typing.Optional[CodType] = jstruct.JStruct[CodType]
    insurance: typing.Optional[InsuranceType] = jstruct.JStruct[InsuranceType]
    messages: typing.Optional[MessagesType] = jstruct.JStruct[MessagesType]
    person: typing.Optional[PersonType] = jstruct.JStruct[PersonType]


@attr.s(auto_attribs=True)
class ReceiverAddressType:
    name1: typing.Optional[str] = None
    name2: typing.Any = None
    companyName: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    addressLine2: typing.Any = None
    addressLine3: typing.Any = None
    interphoneName: typing.Any = None
    floor: typing.Any = None
    doorCode: typing.Any = None
    building: typing.Any = None
    department: typing.Any = None
    zipCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Any = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverContactType:
    contactPerson: typing.Optional[str] = None
    phone1: typing.Optional[str] = None
    phone2: typing.Any = None
    fax: typing.Any = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LegalEntityType:
    businessType: typing.Optional[str] = None
    eori: typing.Optional[str] = None
    vatNumber: typing.Optional[str] = None
    taxIdType: typing.Any = None
    taxIdValue: typing.Any = None


@attr.s(auto_attribs=True)
class ReceiverType:
    address: typing.Optional[ReceiverAddressType] = jstruct.JStruct[ReceiverAddressType]
    contact: typing.Optional[ReceiverContactType] = jstruct.JStruct[ReceiverContactType]
    legalEntity: typing.Optional[LegalEntityType] = jstruct.JStruct[LegalEntityType]


@attr.s(auto_attribs=True)
class CustomerInfosType:
    customerID: typing.Optional[str] = None
    customerAccountNumber: typing.Optional[str] = None
    customerSubAccountNumber: typing.Any = None
    originalCustomerId: typing.Any = None


@attr.s(auto_attribs=True)
class SenderType:
    customerInfos: typing.Optional[CustomerInfosType] = jstruct.JStruct[CustomerInfosType]
    address: typing.Optional[ReceiverAddressType] = jstruct.JStruct[ReceiverAddressType]
    contact: typing.Optional[ReceiverContactType] = jstruct.JStruct[ReceiverContactType]
    legalEntity: typing.Optional[LegalEntityType] = jstruct.JStruct[LegalEntityType]


@attr.s(auto_attribs=True)
class ShipmentInfosType:
    productCode: typing.Optional[str] = None
    shipmentId: typing.Optional[str] = None
    weight: typing.Optional[str] = None
    cifcost: typing.Optional[CustomsAmountType] = jstruct.JStruct[CustomsAmountType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ShipmentRequestElementType:
    numberOfParcels: typing.Optional[str] = None
    shipmentInfos: typing.Optional[ShipmentInfosType] = jstruct.JStruct[ShipmentInfosType]
    sender: typing.Optional[SenderType] = jstruct.JStruct[SenderType]
    receiver: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    parcel: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    international: typing.Optional[InternationalType] = jstruct.JStruct[InternationalType]
    delivery: typing.Optional[DeliveryType] = jstruct.JStruct[DeliveryType]
