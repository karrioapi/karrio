from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class AccountType:
    typeCode: Optional[str] = None
    number: Optional[int] = None


@s(auto_attribs=True)
class AdditionalChargeType:
    value: Optional[int] = None
    caption: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class CustomerReferenceType:
    typeCode: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class DeclarationNoteType:
    value: Optional[str] = None


@s(auto_attribs=True)
class ExporterType:
    id: Optional[int] = None
    code: Optional[str] = None


@s(auto_attribs=True)
class InvoiceType:
    number: Optional[str] = None
    date: Optional[str] = None
    signatureName: Optional[str] = None
    signatureTitle: Optional[str] = None
    signatureImage: Optional[str] = None
    instructions: List[str] = []
    customerDataTextEntries: List[str] = []
    function: Optional[str] = None
    totalNetWeight: Optional[int] = None
    totalGrossWeight: Optional[int] = None
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    termsOfPayment: Optional[str] = None


@s(auto_attribs=True)
class QuantityType:
    value: Optional[int] = None
    unitOfMeasurement: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    netValue: Optional[int] = None
    grossValue: Optional[int] = None


@s(auto_attribs=True)
class LineItemType:
    number: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
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
class BarcodeType:
    position: Optional[str] = None
    symbologyCode: Optional[int] = None
    content: Optional[str] = None
    textBelowBarcode: Optional[str] = None


@s(auto_attribs=True)
class LabelTextType:
    position: Optional[str] = None
    caption: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    typeCode: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    identifiers: List[CustomerReferenceType] = JList[CustomerReferenceType]
    description: Optional[str] = None
    labelBarcodes: List[BarcodeType] = JList[BarcodeType]
    labelText: List[LabelTextType] = JList[LabelTextType]
    labelDescription: Optional[str] = None


@s(auto_attribs=True)
class ContentType:
    packages: List[PackageType] = JList[PackageType]
    isCustomsDeclarable: Optional[bool] = None
    declaredValue: Optional[int] = None
    declaredValueCurrency: Optional[str] = None
    exportDeclaration: Optional[ExportDeclarationType] = JStruct[ExportDeclarationType]
    description: Optional[str] = None
    USFilingTypeValue: Optional[int] = None
    incoterm: Optional[str] = None
    unitOfMeasurement: Optional[str] = None


@s(auto_attribs=True)
class BankDetailType:
    name: Optional[str] = None
    settlementLocalCurrency: Optional[str] = None
    settlementForeignCurrency: Optional[str] = None


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
class RegistrationNumberType:
    typeCode: Optional[str] = None
    number: Optional[str] = None
    issuerCountryCode: Optional[str] = None


@s(auto_attribs=True)
class DetailsType:
    postalAddress: Optional[PostalAddressType] = JStruct[PostalAddressType]
    contactInformation: Optional[ContactInformationType] = JStruct[ContactInformationType]
    registrationNumbers: List[RegistrationNumberType] = JList[RegistrationNumberType]
    bankDetails: List[BankDetailType] = JList[BankDetailType]
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: Optional[DetailsType] = JStruct[DetailsType]
    receiverDetails: Optional[DetailsType] = JStruct[DetailsType]
    buyerDetails: Optional[DetailsType] = JStruct[DetailsType]
    importerDetails: Optional[DetailsType] = JStruct[DetailsType]
    exporterDetails: Optional[DetailsType] = JStruct[DetailsType]
    sellerDetails: Optional[DetailsType] = JStruct[DetailsType]
    payerDetails: Optional[DetailsType] = JStruct[DetailsType]


@s(auto_attribs=True)
class DocumentImageType:
    typeCode: Optional[str] = None
    imageFormat: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class OnDemandDeliveryType:
    deliveryOption: Optional[str] = None
    location: Optional[str] = None
    specialInstructions: Optional[str] = None
    gateCode: Optional[int] = None
    whereToLeave: Optional[str] = None
    neighbourName: Optional[str] = None
    neighbourHouseNumber: Optional[int] = None
    authorizerName: Optional[str] = None
    servicePointId: Optional[str] = None
    requestedDeliveryDate: Optional[str] = None


@s(auto_attribs=True)
class CustomerLogoType:
    fileFormat: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class ImageOptionType:
    typeCode: Optional[str] = None
    templateName: Optional[str] = None
    isRequested: Optional[bool] = None
    hideAccountNumber: Optional[bool] = None
    numberOfCopies: Optional[int] = None
    invoiceType: Optional[str] = None
    languageCode: Optional[str] = None
    encodingFormat: Optional[str] = None
    renderDHLLogo: Optional[bool] = None


@s(auto_attribs=True)
class OutputImagePropertiesType:
    printerDPI: Optional[int] = None
    customerBarcodes: List[BarcodeType] = JList[BarcodeType]
    customerLogos: List[CustomerLogoType] = JList[CustomerLogoType]
    encodingFormat: Optional[str] = None
    imageOptions: List[ImageOptionType] = JList[ImageOptionType]
    splitTransportAndWaybillDocLabels: Optional[bool] = None
    allDocumentsInOneImage: Optional[bool] = None
    splitDocumentsByPages: Optional[bool] = None
    splitInvoiceAndReceipt: Optional[bool] = None


@s(auto_attribs=True)
class ParentShipmentType:
    productCode: Optional[str] = None
    packagesCount: Optional[int] = None


@s(auto_attribs=True)
class PickupType:
    isRequested: Optional[bool] = None
    closeTime: Optional[str] = None
    location: Optional[str] = None
    specialInstructions: List[CustomerReferenceType] = JList[CustomerReferenceType]
    pickupDetails: Optional[DetailsType] = JStruct[DetailsType]
    pickupRequestorDetails: Optional[DetailsType] = JStruct[DetailsType]


@s(auto_attribs=True)
class PrepaidChargeType:
    typeCode: Optional[str] = None
    currency: Optional[str] = None
    value: Optional[int] = None
    method: Optional[str] = None


@s(auto_attribs=True)
class ShipmentNotificationType:
    typeCode: Optional[str] = None
    receiverId: Optional[str] = None
    languageCode: Optional[str] = None
    languageCountryCode: Optional[str] = None
    bespokeMessage: Optional[str] = None


@s(auto_attribs=True)
class DangerousGoodType:
    contentId: Optional[int] = None
    dryIceTotalNetWeight: Optional[int] = None
    unCode: Optional[str] = None


@s(auto_attribs=True)
class ValueAddedServiceType:
    serviceCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    method: Optional[str] = None
    dangerousGoods: List[DangerousGoodType] = JList[DangerousGoodType]


@s(auto_attribs=True)
class ShipmentRequestType:
    plannedShippingDateAndTime: Optional[str] = None
    pickup: Optional[PickupType] = JStruct[PickupType]
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    getRateEstimates: Optional[bool] = None
    accounts: List[AccountType] = JList[AccountType]
    valueAddedServices: List[ValueAddedServiceType] = JList[ValueAddedServiceType]
    outputImageProperties: Optional[OutputImagePropertiesType] = JStruct[OutputImagePropertiesType]
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    identifiers: List[CustomerReferenceType] = JList[CustomerReferenceType]
    customerDetails: Optional[CustomerDetailsType] = JStruct[CustomerDetailsType]
    content: Optional[ContentType] = JStruct[ContentType]
    documentImages: List[DocumentImageType] = JList[DocumentImageType]
    onDemandDelivery: Optional[OnDemandDeliveryType] = JStruct[OnDemandDeliveryType]
    requestOndemandDeliveryURL: Optional[bool] = None
    shipmentNotification: List[ShipmentNotificationType] = JList[ShipmentNotificationType]
    prepaidCharges: List[PrepaidChargeType] = JList[PrepaidChargeType]
    getOptionalInformation: Optional[bool] = None
    parentShipment: Optional[ParentShipmentType] = JStruct[ParentShipmentType]
