import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressType:
    name1: typing.Optional[str] = None
    name2: typing.Optional[str] = None
    street1: typing.Optional[str] = None
    street2: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    postcode: typing.Optional[str] = None
    city1: typing.Optional[str] = None
    stateOrRegion: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactPersonType:
    name: typing.Optional[str] = None
    emailAddress: typing.Optional[str] = None
    phoneCountryPrefix: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    mobileCountryPrefix: typing.Optional[str] = None
    mobileNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ConsigneeType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contactPerson: typing.Optional[ContactPersonType] = jstruct.JStruct[ContactPersonType]


@attr.s(auto_attribs=True)
class ExporterType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contactPerson: typing.Optional[ContactPersonType] = jstruct.JStruct[ContactPersonType]
    eoriNumber: typing.Optional[str] = None
    swissUid: typing.Optional[str] = None
    taxId: typing.Optional[str] = None
    vatRegistrationNumber: typing.Optional[str] = None
    isCommercial: typing.Optional[bool] = None
    authorizationNumber: typing.Optional[str] = None
    loadingPlaceCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ImporterType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contactPerson: typing.Optional[ContactPersonType] = jstruct.JStruct[ContactPersonType]
    eoriNumber: typing.Optional[str] = None
    taxId: typing.Optional[str] = None
    isCommercial: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ValueType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InvoiceType:
    invoiceNumber: typing.Optional[str] = None
    invoiceDate: typing.Optional[str] = None
    totalGoodsValue: typing.Optional[ValueType] = jstruct.JStruct[ValueType]


@attr.s(auto_attribs=True)
class TotalGrossWeightType:
    amount: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BeType:
    regionOfOrigin: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NationalCustomsFieldsType:
    de: typing.Optional[BeType] = jstruct.JStruct[BeType]
    be: typing.Optional[BeType] = jstruct.JStruct[BeType]


@attr.s(auto_attribs=True)
class LineItemType:
    quantity: typing.Optional[TotalGrossWeightType] = jstruct.JStruct[TotalGrossWeightType]
    commodityCode: typing.Optional[str] = None
    goodsDescription: typing.Optional[str] = None
    countryOfOrigin: typing.Optional[str] = None
    valueInInvoiceCurrency: typing.Optional[float] = None
    preferentialTrade: typing.Any = None
    statisticalValue: typing.Optional[ValueType] = jstruct.JStruct[ValueType]
    statisticalQuantity: typing.Optional[float] = None
    nationalCustomsFields: typing.Optional[NationalCustomsFieldsType] = jstruct.JStruct[NationalCustomsFieldsType]
    grossWeight: typing.Optional[TotalGrossWeightType] = jstruct.JStruct[TotalGrossWeightType]
    netWeight: typing.Optional[TotalGrossWeightType] = jstruct.JStruct[TotalGrossWeightType]


@attr.s(auto_attribs=True)
class LinkedDocumentType:
    documentId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsConsignmentRequestType:
    parcelNumbers: typing.Optional[typing.List[str]] = None
    glsIncotermCode: typing.Optional[str] = None
    totalGrossWeight: typing.Optional[TotalGrossWeightType] = jstruct.JStruct[TotalGrossWeightType]
    exporter: typing.Optional[ExporterType] = jstruct.JStruct[ExporterType]
    importer: typing.Optional[ImporterType] = jstruct.JStruct[ImporterType]
    consignee: typing.Optional[ConsigneeType] = jstruct.JStruct[ConsigneeType]
    invoice: typing.Optional[InvoiceType] = jstruct.JStruct[InvoiceType]
    lineItems: typing.Optional[typing.List[LineItemType]] = jstruct.JList[LineItemType]
    customerReference: typing.Optional[str] = None
    additionalInformation: typing.Optional[str] = None
    isExportDeclarationRequested: typing.Optional[bool] = None
    exportDeclarationNumbers: typing.Optional[typing.List[str]] = None
    transitMRNs: typing.Optional[typing.List[str]] = None
    transitType: typing.Optional[str] = None
    saveAsDraft: typing.Optional[bool] = None
    linkedDocuments: typing.Optional[typing.List[LinkedDocumentType]] = jstruct.JList[LinkedDocumentType]
