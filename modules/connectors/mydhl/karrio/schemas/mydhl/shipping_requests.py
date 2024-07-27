from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class AccountType:
    typeCode: Optional[str] = None
    number: Optional[str] = None


@s(auto_attribs=True)
class AdditionalChargeType:
    value: Optional[float] = None
    caption: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class CustomerReferenceType:
    value: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class DeclarationNoteType:
    value: Optional[str] = None


@s(auto_attribs=True)
class ExporterType:
    id: Optional[int] = None
    code: Optional[str] = None


@s(auto_attribs=True)
class IndicativeCustomsValuesType:
    importCustomsDutyValue: Optional[float] = None
    importTaxesValue: Optional[float] = None


@s(auto_attribs=True)
class InvoiceType:
    number: Optional[str] = None
    date: Optional[str] = None
    instructions: List[str] = []
    totalNetWeight: Optional[float] = None
    totalGrossWeight: Optional[float] = None
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    termsOfPayment: Optional[str] = None
    indicativeCustomsValues: Optional[IndicativeCustomsValuesType] = JStruct[IndicativeCustomsValuesType]
    customerDataTextEntries: List[str] = []


@s(auto_attribs=True)
class QuantityType:
    value: Optional[int] = None
    unitOfMeasurement: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    netValue: Optional[float] = None
    grossValue: Optional[float] = None


@s(auto_attribs=True)
class LineItemType:
    number: Optional[int] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[QuantityType] = JStruct[QuantityType]
    commodityCodes: List[CustomerReferenceType] = JList[CustomerReferenceType]
    exportReasonType: Optional[str] = None
    manufacturerCountry: Optional[str] = None
    exportControlClassificationNumber: Optional[str] = None
    weight: Optional[WeightType] = JStruct[WeightType]
    isTaxesPaid: Optional[bool] = None
    additionalInformation: List[str] = []
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    customsDocuments: List[CustomerReferenceType] = JList[CustomerReferenceType]


@s(auto_attribs=True)
class ExportDeclarationType:
    lineItems: List[LineItemType] = JList[LineItemType]
    invoice: Optional[InvoiceType] = JStruct[InvoiceType]
    remarks: List[DeclarationNoteType] = JList[DeclarationNoteType]
    additionalCharges: List[AdditionalChargeType] = JList[AdditionalChargeType]
    destinationPortName: Optional[str] = None
    placeOfIncoterm: Optional[str] = None
    payerVATNumber: Optional[str] = None
    recipientReference: Optional[str] = None
    exporter: Optional[ExporterType] = JStruct[ExporterType]
    packageMarks: Optional[str] = None
    declarationNotes: List[DeclarationNoteType] = JList[DeclarationNoteType]
    exportReference: Optional[str] = None
    exportReason: Optional[str] = None
    exportReasonType: Optional[str] = None
    licenses: List[CustomerReferenceType] = JList[CustomerReferenceType]
    shipmentType: Optional[str] = None
    customsDocuments: List[CustomerReferenceType] = JList[CustomerReferenceType]


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
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    description: Optional[str] = None
    labelDescription: Optional[str] = None


@s(auto_attribs=True)
class ContentType:
    packages: List[PackageType] = JList[PackageType]
    isCustomsDeclarable: Optional[bool] = None
    declaredValue: Optional[float] = None
    declaredValueCurrency: Optional[str] = None
    exportDeclaration: Optional[ExportDeclarationType] = JStruct[ExportDeclarationType]
    description: Optional[str] = None
    USFilingTypeValue: Optional[int] = None
    incoterm: Optional[str] = None
    unitOfMeasurement: Optional[str] = None


@s(auto_attribs=True)
class ContactInformationType:
    phone: Optional[str] = None
    mobilePhone: Optional[str] = None
    companyName: Optional[str] = None
    fullName: Optional[str] = None
    email: Optional[str] = None


@s(auto_attribs=True)
class PostalAddressType:
    cityName: Optional[str] = None
    countryCode: Optional[str] = None
    postalCode: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    countyName: Optional[str] = None
    addressLine3: Optional[str] = None
    countryName: Optional[str] = None
    provinceCode: Optional[str] = None


@s(auto_attribs=True)
class RegistrationNumberType:
    issuerCountryCode: Optional[str] = None
    number: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class BuyerDetailsClassType:
    postalAddress: Optional[PostalAddressType] = JStruct[PostalAddressType]
    contactInformation: Optional[ContactInformationType] = JStruct[ContactInformationType]
    registrationNumbers: List[RegistrationNumberType] = JList[RegistrationNumberType]
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class BankDetailType:
    name: Optional[str] = None
    settlementLocalCurrency: Optional[str] = None
    settlementForeignCurrency: Optional[str] = None


@s(auto_attribs=True)
class ReceiverDetailsClassType:
    postalAddress: Optional[PostalAddressType] = JStruct[PostalAddressType]
    contactInformation: Optional[ContactInformationType] = JStruct[ContactInformationType]
    registrationNumbers: List[RegistrationNumberType] = JList[RegistrationNumberType]
    bankDetails: List[BankDetailType] = JList[BankDetailType]
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: Optional[ReceiverDetailsClassType] = JStruct[ReceiverDetailsClassType]
    receiverDetails: Optional[ReceiverDetailsClassType] = JStruct[ReceiverDetailsClassType]
    buyerDetails: Optional[BuyerDetailsClassType] = JStruct[BuyerDetailsClassType]
    importerDetails: Optional[BuyerDetailsClassType] = JStruct[BuyerDetailsClassType]
    exporterDetails: Optional[BuyerDetailsClassType] = JStruct[BuyerDetailsClassType]
    sellerDetails: Optional[BuyerDetailsClassType] = JStruct[BuyerDetailsClassType]


@s(auto_attribs=True)
class DocumentImageType:
    typeCode: Optional[str] = None
    imageFormat: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class EstimatedDeliveryDateType:
    isRequested: Optional[bool] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class ImageOptionType:
    typeCode: Optional[str] = None
    templateName: Optional[str] = None
    isRequested: Optional[bool] = None
    invoiceType: Optional[str] = None
    languageCode: Optional[str] = None
    languageCountryCode: Optional[str] = None
    hideAccountNumber: Optional[bool] = None
    numberOfCopies: Optional[int] = None
    renderDHLLogo: Optional[bool] = None
    fitLabelsToA4: Optional[bool] = None
    encodingFormat: Optional[str] = None


@s(auto_attribs=True)
class OutputImagePropertiesType:
    printerDPI: Optional[int] = None
    encodingFormat: Optional[str] = None
    imageOptions: List[ImageOptionType] = JList[ImageOptionType]
    splitTransportAndWaybillDocLabels: Optional[bool] = None
    allDocumentsInOneImage: Optional[bool] = None
    splitDocumentsByPages: Optional[bool] = None
    splitInvoiceAndReceipt: Optional[bool] = None
    receiptAndLabelsInOneImage: Optional[bool] = None


@s(auto_attribs=True)
class PickupType:
    isRequested: Optional[bool] = None
    closeTime: Optional[str] = None
    location: Optional[str] = None
    specialInstructions: List[CustomerReferenceType] = JList[CustomerReferenceType]


@s(auto_attribs=True)
class ShipmentNotificationType:
    typeCode: Optional[str] = None
    receiverId: Optional[str] = None
    languageCode: Optional[str] = None
    languageCountryCode: Optional[str] = None
    bespokeMessage: Optional[str] = None


@s(auto_attribs=True)
class ValueAddedServiceType:
    serviceCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    method: Optional[str] = None


@s(auto_attribs=True)
class ShippingRequestType:
    plannedShippingDateAndTime: Optional[str] = None
    pickup: Optional[PickupType] = JStruct[PickupType]
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    getRateEstimates: Optional[bool] = None
    accounts: List[AccountType] = JList[AccountType]
    valueAddedServices: List[ValueAddedServiceType] = JList[ValueAddedServiceType]
    outputImageProperties: Optional[OutputImagePropertiesType] = JStruct[OutputImagePropertiesType]
    customerDetails: Optional[CustomerDetailsType] = JStruct[CustomerDetailsType]
    content: Optional[ContentType] = JStruct[ContentType]
    shipmentNotification: List[ShipmentNotificationType] = JList[ShipmentNotificationType]
    getTransliteratedResponse: Optional[bool] = None
    estimatedDeliveryDate: Optional[EstimatedDeliveryDateType] = JStruct[EstimatedDeliveryDateType]
    getAdditionalInformation: List[EstimatedDeliveryDateType] = JList[EstimatedDeliveryDateType]
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    documentImages: List[DocumentImageType] = JList[DocumentImageType]
    identifiers: List[CustomerReferenceType] = JList[CustomerReferenceType]
