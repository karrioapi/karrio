import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdditionalChargeType:
    value: typing.Optional[float] = None
    caption: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerReferenceType:
    value: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeclarationNoteType:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExporterType:
    id: typing.Optional[int] = None
    code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IndicativeCustomsValuesType:
    importCustomsDutyValue: typing.Optional[float] = None
    importTaxesValue: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class InvoiceType:
    number: typing.Optional[str] = None
    date: typing.Optional[str] = None
    instructions: typing.Optional[typing.List[str]] = None
    totalNetWeight: typing.Optional[float] = None
    totalGrossWeight: typing.Optional[float] = None
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    termsOfPayment: typing.Optional[str] = None
    indicativeCustomsValues: typing.Optional[IndicativeCustomsValuesType] = jstruct.JStruct[IndicativeCustomsValuesType]
    customerDataTextEntries: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class QuantityType:
    value: typing.Optional[int] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    netValue: typing.Optional[float] = None
    grossValue: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class LineItemType:
    number: typing.Optional[int] = None
    description: typing.Optional[str] = None
    price: typing.Optional[float] = None
    quantity: typing.Optional[QuantityType] = jstruct.JStruct[QuantityType]
    commodityCodes: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    exportReasonType: typing.Optional[str] = None
    manufacturerCountry: typing.Optional[str] = None
    exportControlClassificationNumber: typing.Optional[str] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    isTaxesPaid: typing.Optional[bool] = None
    additionalInformation: typing.Optional[typing.List[str]] = None
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    customsDocuments: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]


@attr.s(auto_attribs=True)
class ExportDeclarationType:
    lineItems: typing.Optional[typing.List[LineItemType]] = jstruct.JList[LineItemType]
    invoice: typing.Optional[InvoiceType] = jstruct.JStruct[InvoiceType]
    remarks: typing.Optional[typing.List[DeclarationNoteType]] = jstruct.JList[DeclarationNoteType]
    additionalCharges: typing.Optional[typing.List[AdditionalChargeType]] = jstruct.JList[AdditionalChargeType]
    destinationPortName: typing.Optional[str] = None
    placeOfIncoterm: typing.Optional[str] = None
    payerVATNumber: typing.Optional[str] = None
    recipientReference: typing.Optional[str] = None
    exporter: typing.Optional[ExporterType] = jstruct.JStruct[ExporterType]
    packageMarks: typing.Optional[str] = None
    declarationNotes: typing.Optional[typing.List[DeclarationNoteType]] = jstruct.JList[DeclarationNoteType]
    exportReference: typing.Optional[str] = None
    exportReason: typing.Optional[str] = None
    exportReasonType: typing.Optional[str] = None
    licenses: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    shipmentType: typing.Optional[str] = None
    customsDocuments: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]


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
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    description: typing.Optional[str] = None
    labelDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContentType:
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    isCustomsDeclarable: typing.Optional[bool] = None
    declaredValue: typing.Optional[float] = None
    declaredValueCurrency: typing.Optional[str] = None
    exportDeclaration: typing.Optional[ExportDeclarationType] = jstruct.JStruct[ExportDeclarationType]
    description: typing.Optional[str] = None
    USFilingTypeValue: typing.Optional[int] = None
    incoterm: typing.Optional[str] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactInformationType:
    phone: typing.Optional[str] = None
    mobilePhone: typing.Optional[str] = None
    companyName: typing.Optional[str] = None
    fullName: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PostalAddressType:
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    countyName: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    countryName: typing.Optional[str] = None
    provinceCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RegistrationNumberType:
    issuerCountryCode: typing.Optional[str] = None
    number: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BuyerDetailsClassType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]
    registrationNumbers: typing.Optional[typing.List[RegistrationNumberType]] = jstruct.JList[RegistrationNumberType]
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BankDetailType:
    name: typing.Optional[str] = None
    settlementLocalCurrency: typing.Optional[str] = None
    settlementForeignCurrency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverDetailsClassType:
    postalAddress: typing.Optional[PostalAddressType] = jstruct.JStruct[PostalAddressType]
    contactInformation: typing.Optional[ContactInformationType] = jstruct.JStruct[ContactInformationType]
    registrationNumbers: typing.Optional[typing.List[RegistrationNumberType]] = jstruct.JList[RegistrationNumberType]
    bankDetails: typing.Optional[typing.List[BankDetailType]] = jstruct.JList[BankDetailType]
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[ReceiverDetailsClassType] = jstruct.JStruct[ReceiverDetailsClassType]
    receiverDetails: typing.Optional[ReceiverDetailsClassType] = jstruct.JStruct[ReceiverDetailsClassType]
    buyerDetails: typing.Optional[BuyerDetailsClassType] = jstruct.JStruct[BuyerDetailsClassType]
    importerDetails: typing.Optional[BuyerDetailsClassType] = jstruct.JStruct[BuyerDetailsClassType]
    exporterDetails: typing.Optional[BuyerDetailsClassType] = jstruct.JStruct[BuyerDetailsClassType]
    sellerDetails: typing.Optional[BuyerDetailsClassType] = jstruct.JStruct[BuyerDetailsClassType]


@attr.s(auto_attribs=True)
class DocumentImageType:
    typeCode: typing.Optional[str] = None
    imageFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EstimatedDeliveryDateType:
    isRequested: typing.Optional[bool] = None
    typeCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ImageOptionType:
    typeCode: typing.Optional[str] = None
    templateName: typing.Optional[str] = None
    isRequested: typing.Optional[bool] = None
    invoiceType: typing.Optional[str] = None
    languageCode: typing.Optional[str] = None
    languageCountryCode: typing.Optional[str] = None
    hideAccountNumber: typing.Optional[bool] = None
    numberOfCopies: typing.Optional[int] = None
    renderDHLLogo: typing.Optional[bool] = None
    fitLabelsToA4: typing.Optional[bool] = None
    encodingFormat: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OutputImagePropertiesType:
    printerDPI: typing.Optional[int] = None
    encodingFormat: typing.Optional[str] = None
    imageOptions: typing.Optional[typing.List[ImageOptionType]] = jstruct.JList[ImageOptionType]
    splitTransportAndWaybillDocLabels: typing.Optional[bool] = None
    allDocumentsInOneImage: typing.Optional[bool] = None
    splitDocumentsByPages: typing.Optional[bool] = None
    splitInvoiceAndReceipt: typing.Optional[bool] = None
    receiptAndLabelsInOneImage: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class PickupType:
    isRequested: typing.Optional[bool] = None
    closeTime: typing.Optional[str] = None
    location: typing.Optional[str] = None
    specialInstructions: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]


@attr.s(auto_attribs=True)
class ShipmentNotificationType:
    typeCode: typing.Optional[str] = None
    receiverId: typing.Optional[str] = None
    languageCode: typing.Optional[str] = None
    languageCountryCode: typing.Optional[str] = None
    bespokeMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValueAddedServiceType:
    serviceCode: typing.Optional[str] = None
    value: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    method: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRequestType:
    plannedShippingDateAndTime: typing.Optional[str] = None
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    getRateEstimates: typing.Optional[bool] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    valueAddedServices: typing.Optional[typing.List[ValueAddedServiceType]] = jstruct.JList[ValueAddedServiceType]
    outputImageProperties: typing.Optional[OutputImagePropertiesType] = jstruct.JStruct[OutputImagePropertiesType]
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    content: typing.Optional[ContentType] = jstruct.JStruct[ContentType]
    shipmentNotification: typing.Optional[typing.List[ShipmentNotificationType]] = jstruct.JList[ShipmentNotificationType]
    getTransliteratedResponse: typing.Optional[bool] = None
    estimatedDeliveryDate: typing.Optional[EstimatedDeliveryDateType] = jstruct.JStruct[EstimatedDeliveryDateType]
    getAdditionalInformation: typing.Optional[typing.List[EstimatedDeliveryDateType]] = jstruct.JList[EstimatedDeliveryDateType]
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    documentImages: typing.Optional[typing.List[DocumentImageType]] = jstruct.JList[DocumentImageType]
    identifiers: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
