from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class Account:
    typeCode: Optional[str] = None
    number: Optional[int] = None


@s(auto_attribs=True)
class AdditionalCharge:
    value: Optional[int] = None
    caption: Optional[str] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class CustomerReference:
    typeCode: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class DeclarationNote:
    value: Optional[str] = None


@s(auto_attribs=True)
class Exporter:
    id: Optional[int] = None
    code: Optional[str] = None


@s(auto_attribs=True)
class Invoice:
    number: Optional[str] = None
    date: Optional[str] = None
    signatureName: Optional[str] = None
    signatureTitle: Optional[str] = None
    signatureImage: Optional[str] = None
    instructions: List[str] = JList[str]
    customerDataTextEntries: List[str] = JList[str]
    function: Optional[str] = None
    totalNetWeight: Optional[int] = None
    totalGrossWeight: Optional[int] = None
    customerReferences: List[CustomerReference] = JList[CustomerReference]
    termsOfPayment: Optional[str] = None


@s(auto_attribs=True)
class Quantity:
    value: Optional[int] = None
    unitOfMeasurement: Optional[str] = None


@s(auto_attribs=True)
class Weight:
    netValue: Optional[int] = None
    grossValue: Optional[int] = None


@s(auto_attribs=True)
class LineItem:
    number: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[Quantity] = JStruct[Quantity]
    commodityCodes: List[CustomerReference] = JList[CustomerReference]
    exportReasonType: Optional[str] = None
    manufacturerCountry: Optional[str] = None
    exportControlClassificationNumber: Optional[str] = None
    weight: Optional[Weight] = JStruct[Weight]
    isTaxesPaid: Optional[bool] = None
    additionalInformation: List[str] = JList[str]
    customerReferences: List[CustomerReference] = JList[CustomerReference]
    customsDocuments: List[CustomerReference] = JList[CustomerReference]


@s(auto_attribs=True)
class ExportDeclaration:
    lineItems: List[LineItem] = JList[LineItem]
    invoice: Optional[Invoice] = JStruct[Invoice]
    remarks: List[DeclarationNote] = JList[DeclarationNote]
    additionalCharges: List[AdditionalCharge] = JList[AdditionalCharge]
    destinationPortName: Optional[str] = None
    placeOfIncoterm: Optional[str] = None
    payerVATNumber: Optional[str] = None
    recipientReference: Optional[str] = None
    exporter: Optional[Exporter] = JStruct[Exporter]
    packageMarks: Optional[str] = None
    declarationNotes: List[DeclarationNote] = JList[DeclarationNote]
    exportReference: Optional[str] = None
    exportReason: Optional[str] = None
    exportReasonType: Optional[str] = None
    licenses: List[CustomerReference] = JList[CustomerReference]
    shipmentType: Optional[str] = None
    customsDocuments: List[CustomerReference] = JList[CustomerReference]


@s(auto_attribs=True)
class Dimensions:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@s(auto_attribs=True)
class Barcode:
    position: Optional[str] = None
    symbologyCode: Optional[int] = None
    content: Optional[str] = None
    textBelowBarcode: Optional[str] = None


@s(auto_attribs=True)
class LabelText:
    position: Optional[str] = None
    caption: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class Package:
    typeCode: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[Dimensions] = JStruct[Dimensions]
    customerReferences: List[CustomerReference] = JList[CustomerReference]
    identifiers: List[CustomerReference] = JList[CustomerReference]
    description: Optional[str] = None
    labelBarcodes: List[Barcode] = JList[Barcode]
    labelText: List[LabelText] = JList[LabelText]
    labelDescription: Optional[str] = None


@s(auto_attribs=True)
class Content:
    packages: List[Package] = JList[Package]
    isCustomsDeclarable: Optional[bool] = None
    declaredValue: Optional[int] = None
    declaredValueCurrency: Optional[str] = None
    exportDeclaration: Optional[ExportDeclaration] = JStruct[ExportDeclaration]
    description: Optional[str] = None
    USFilingTypeValue: Optional[int] = None
    incoterm: Optional[str] = None
    unitOfMeasurement: Optional[str] = None


@s(auto_attribs=True)
class BankDetail:
    name: Optional[str] = None
    settlementLocalCurrency: Optional[str] = None
    settlementForeignCurrency: Optional[str] = None


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
class RegistrationNumber:
    typeCode: Optional[str] = None
    number: Optional[str] = None
    issuerCountryCode: Optional[str] = None


@s(auto_attribs=True)
class Details:
    postalAddress: Optional[PostalAddress] = JStruct[PostalAddress]
    contactInformation: Optional[ContactInformation] = JStruct[ContactInformation]
    registrationNumbers: List[RegistrationNumber] = JList[RegistrationNumber]
    bankDetails: List[BankDetail] = JList[BankDetail]
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class CustomerDetails:
    shipperDetails: Optional[Details] = JStruct[Details]
    receiverDetails: Optional[Details] = JStruct[Details]
    buyerDetails: Optional[Details] = JStruct[Details]
    importerDetails: Optional[Details] = JStruct[Details]
    exporterDetails: Optional[Details] = JStruct[Details]
    sellerDetails: Optional[Details] = JStruct[Details]
    payerDetails: Optional[Details] = JStruct[Details]


@s(auto_attribs=True)
class DocumentImage:
    typeCode: Optional[str] = None
    imageFormat: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class OnDemandDelivery:
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
class CustomerLogo:
    fileFormat: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class ImageOption:
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
class OutputImageProperties:
    printerDPI: Optional[int] = None
    customerBarcodes: List[Barcode] = JList[Barcode]
    customerLogos: List[CustomerLogo] = JList[CustomerLogo]
    encodingFormat: Optional[str] = None
    imageOptions: List[ImageOption] = JList[ImageOption]
    splitTransportAndWaybillDocLabels: Optional[bool] = None
    allDocumentsInOneImage: Optional[bool] = None
    splitDocumentsByPages: Optional[bool] = None
    splitInvoiceAndReceipt: Optional[bool] = None


@s(auto_attribs=True)
class ParentShipment:
    productCode: Optional[str] = None
    packagesCount: Optional[int] = None


@s(auto_attribs=True)
class Pickup:
    isRequested: Optional[bool] = None
    closeTime: Optional[str] = None
    location: Optional[str] = None
    specialInstructions: List[CustomerReference] = JList[CustomerReference]
    pickupDetails: Optional[Details] = JStruct[Details]
    pickupRequestorDetails: Optional[Details] = JStruct[Details]


@s(auto_attribs=True)
class PrepaidCharge:
    typeCode: Optional[str] = None
    currency: Optional[str] = None
    value: Optional[int] = None
    method: Optional[str] = None


@s(auto_attribs=True)
class ShipmentNotification:
    typeCode: Optional[str] = None
    receiverId: Optional[str] = None
    languageCode: Optional[str] = None
    languageCountryCode: Optional[str] = None
    bespokeMessage: Optional[str] = None


@s(auto_attribs=True)
class DangerousGood:
    contentId: Optional[int] = None
    dryIceTotalNetWeight: Optional[int] = None
    unCode: Optional[str] = None


@s(auto_attribs=True)
class ValueAddedService:
    serviceCode: Optional[str] = None
    value: Optional[int] = None
    currency: Optional[str] = None
    method: Optional[str] = None
    dangerousGoods: List[DangerousGood] = JList[DangerousGood]


@s(auto_attribs=True)
class CreateShipmentRequest:
    plannedShippingDateAndTime: Optional[str] = None
    pickup: Optional[Pickup] = JStruct[Pickup]
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    getRateEstimates: Optional[bool] = None
    accounts: List[Account] = JList[Account]
    valueAddedServices: List[ValueAddedService] = JList[ValueAddedService]
    outputImageProperties: Optional[OutputImageProperties] = JStruct[OutputImageProperties]
    customerReferences: List[CustomerReference] = JList[CustomerReference]
    identifiers: List[CustomerReference] = JList[CustomerReference]
    customerDetails: Optional[CustomerDetails] = JStruct[CustomerDetails]
    content: Optional[Content] = JStruct[Content]
    documentImages: List[DocumentImage] = JList[DocumentImage]
    onDemandDelivery: Optional[OnDemandDelivery] = JStruct[OnDemandDelivery]
    requestOndemandDeliveryURL: Optional[bool] = None
    shipmentNotification: List[ShipmentNotification] = JList[ShipmentNotification]
    prepaidCharges: List[PrepaidCharge] = JList[PrepaidCharge]
    getOptionalInformation: Optional[bool] = None
    parentShipment: Optional[ParentShipment] = JStruct[ParentShipment]
