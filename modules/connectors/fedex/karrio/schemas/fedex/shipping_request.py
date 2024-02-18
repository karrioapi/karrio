from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccountNumberType:
    value: Optional[str] = None


@s(auto_attribs=True)
class AddressType:
    streetLines: List[str] = []
    city: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    postalCode: Optional[int] = None
    countryCode: Optional[str] = None
    residential: Optional[bool] = None


@s(auto_attribs=True)
class BrokerContactType:
    personName: Optional[str] = None
    emailAddress: Optional[str] = None
    phoneNumber: Optional[int] = None
    phoneExtension: Optional[int] = None
    companyName: Optional[str] = None
    faxNumber: Optional[int] = None


@s(auto_attribs=True)
class TinType:
    number: Optional[str] = None
    tinType: Optional[str] = None
    usage: Optional[str] = None
    effectiveDate: Optional[str] = None
    expirationDate: Optional[str] = None


@s(auto_attribs=True)
class BrokerBrokerType:
    address: Optional[AddressType] = JStruct[AddressType]
    contact: Optional[BrokerContactType] = JStruct[BrokerContactType]
    accountNumber: Optional[AccountNumberType] = JStruct[AccountNumberType]
    tins: List[TinType] = JList[TinType]
    deliveryInstructions: Optional[str] = None


@s(auto_attribs=True)
class BrokerElementType:
    broker: Optional[BrokerBrokerType] = JStruct[BrokerBrokerType]
    type: Optional[str] = None


@s(auto_attribs=True)
class CustomerReferenceType:
    customerReferenceType: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class CommercialInvoiceEmailNotificationDetailType:
    emailAddress: Optional[str] = None
    type: Optional[str] = None
    recipientType: Optional[str] = None


@s(auto_attribs=True)
class TotalDeclaredValueType:
    amount: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class CommercialInvoiceType:
    originatorName: Optional[str] = None
    comments: List[str] = []
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    taxesOrMiscellaneousCharge: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    taxesOrMiscellaneousChargeType: Optional[str] = None
    freightCharge: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    packingCosts: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    handlingCosts: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    declarationStatement: Optional[str] = None
    termsOfSale: Optional[str] = None
    specialInstructions: Optional[str] = None
    shipmentPurpose: Optional[str] = None
    emailNotificationDetail: Optional[CommercialInvoiceEmailNotificationDetailType] = JStruct[CommercialInvoiceEmailNotificationDetailType]


@s(auto_attribs=True)
class AdditionalMeasureType:
    quantity: Optional[float] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class CustomsValueType:
    amount: Optional[str] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class UsmcaDetailType:
    originCriterion: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    units: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class CommodityType:
    unitPrice: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    additionalMeasures: List[AdditionalMeasureType] = JList[AdditionalMeasureType]
    numberOfPieces: Optional[int] = None
    quantity: Optional[int] = None
    quantityUnits: Optional[str] = None
    customsValue: Optional[CustomsValueType] = JStruct[CustomsValueType]
    countryOfManufacture: Optional[str] = None
    cIMarksAndNumbers: Optional[int] = None
    harmonizedCode: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    weight: Optional[WeightType] = JStruct[WeightType]
    exportLicenseNumber: Optional[int] = None
    exportLicenseExpirationDate: Optional[str] = None
    partNumber: Optional[int] = None
    purpose: Optional[str] = None
    usmcaDetail: Optional[UsmcaDetailType] = JStruct[UsmcaDetailType]


@s(auto_attribs=True)
class CustomsOptionType:
    description: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class UsmcaLowValueStatementDetailType:
    countryOfOriginLowValueDocumentRequested: Optional[bool] = None
    customsRole: Optional[str] = None


@s(auto_attribs=True)
class DeclarationStatementDetailType:
    usmcaLowValueStatementDetail: Optional[UsmcaLowValueStatementDetailType] = JStruct[UsmcaLowValueStatementDetailType]


@s(auto_attribs=True)
class BillingDetailsType:
    billingCode: Optional[str] = None
    billingType: Optional[str] = None
    aliasId: Optional[str] = None
    accountNickname: Optional[str] = None
    accountNumber: Optional[str] = None
    accountNumberCountryCode: Optional[str] = None


@s(auto_attribs=True)
class ResponsiblePartyContactType:
    personName: Optional[str] = None
    emailAddress: Optional[str] = None
    phoneNumber: Optional[str] = None
    phoneExtension: Optional[str] = None
    companyName: Optional[str] = None
    faxNumber: Optional[str] = None


@s(auto_attribs=True)
class ResponsiblePartyType:
    address: Optional[AddressType] = JStruct[AddressType]
    contact: Optional[ResponsiblePartyContactType] = JStruct[ResponsiblePartyContactType]
    accountNumber: Optional[AccountNumberType] = JStruct[AccountNumberType]
    tins: List[TinType] = JList[TinType]


@s(auto_attribs=True)
class PayorType:
    responsibleParty: Optional[ResponsiblePartyType] = JStruct[ResponsiblePartyType]


@s(auto_attribs=True)
class DutiesPaymentType:
    payor: Optional[PayorType] = JStruct[PayorType]
    billingDetails: Optional[BillingDetailsType] = JStruct[BillingDetailsType]
    paymentType: Optional[str] = None


@s(auto_attribs=True)
class DestinationControlDetailType:
    endUser: Optional[str] = None
    statementTypes: Optional[str] = None
    destinationCountries: List[str] = []


@s(auto_attribs=True)
class ExportDetailType:
    destinationControlDetail: Optional[DestinationControlDetailType] = JStruct[DestinationControlDetailType]
    b13AFilingOption: Optional[str] = None
    exportComplianceStatement: Optional[str] = None
    permitNumber: Optional[int] = None


@s(auto_attribs=True)
class ShipperType:
    address: Optional[AddressType] = JStruct[AddressType]
    contact: Optional[ResponsiblePartyContactType] = JStruct[ResponsiblePartyContactType]
    accountNumber: Optional[AccountNumberType] = JStruct[AccountNumberType]
    tins: List[TinType] = JList[TinType]
    deliveryInstructions: Optional[str] = None


@s(auto_attribs=True)
class RecipientCustomsIDType:
    type: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class CustomsClearanceDetailType:
    regulatoryControls: Optional[str] = None
    brokers: List[BrokerElementType] = JList[BrokerElementType]
    commercialInvoice: Optional[CommercialInvoiceType] = JStruct[CommercialInvoiceType]
    freightOnValue: Optional[str] = None
    dutiesPayment: Optional[DutiesPaymentType] = JStruct[DutiesPaymentType]
    commodities: List[CommodityType] = JList[CommodityType]
    isDocumentOnly: Optional[bool] = None
    recipientCustomsId: Optional[RecipientCustomsIDType] = JStruct[RecipientCustomsIDType]
    customsOption: Optional[CustomsOptionType] = JStruct[CustomsOptionType]
    importerOfRecord: Optional[ShipperType] = JStruct[ShipperType]
    generatedDocumentLocale: Optional[str] = None
    exportDetail: Optional[ExportDetailType] = JStruct[ExportDetailType]
    totalCustomsValue: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    partiesToTransactionAreRelated: Optional[bool] = None
    declarationStatementDetail: Optional[DeclarationStatementDetailType] = JStruct[DeclarationStatementDetailType]
    insuranceCharge: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]


@s(auto_attribs=True)
class EmailNotificationRecipientType:
    name: Optional[str] = None
    emailNotificationRecipientType: Optional[str] = None
    emailAddress: Optional[str] = None
    notificationFormatType: Optional[str] = None
    notificationType: Optional[str] = None
    locale: Optional[str] = None
    notificationEventType: List[str] = []


@s(auto_attribs=True)
class RequestedShipmentEmailNotificationDetailType:
    aggregationType: Optional[str] = None
    emailNotificationRecipients: List[EmailNotificationRecipientType] = JList[EmailNotificationRecipientType]
    personalMessage: Optional[str] = None


@s(auto_attribs=True)
class ExpressFreightDetailType:
    bookingConfirmationNumber: Optional[str] = None
    shippersLoadAndCount: Optional[int] = None
    packingListEnclosed: Optional[bool] = None


@s(auto_attribs=True)
class AdditionalLabelType:
    type: Optional[str] = None
    count: Optional[int] = None


@s(auto_attribs=True)
class SpecificationType:
    zoneNumber: Optional[int] = None
    header: Optional[str] = None
    dataField: Optional[str] = None
    literalValue: Optional[str] = None
    justification: Optional[str] = None


@s(auto_attribs=True)
class BarcodedType:
    symbology: Optional[str] = None
    specification: Optional[SpecificationType] = JStruct[SpecificationType]


@s(auto_attribs=True)
class Zone001Type:
    docTabZoneSpecifications: List[SpecificationType] = JList[SpecificationType]


@s(auto_attribs=True)
class DocTabContentType:
    docTabContentType: Optional[str] = None
    zone001: Optional[Zone001Type] = JStruct[Zone001Type]
    barcoded: Optional[BarcodedType] = JStruct[BarcodedType]


@s(auto_attribs=True)
class RegulatoryLabelType:
    generationOptions: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class CustomerSpecifiedDetailType:
    maskedData: List[str] = []
    regulatoryLabels: List[RegulatoryLabelType] = JList[RegulatoryLabelType]
    additionalLabels: List[AdditionalLabelType] = JList[AdditionalLabelType]
    docTabContent: Optional[DocTabContentType] = JStruct[DocTabContentType]


@s(auto_attribs=True)
class OriginType:
    address: Optional[AddressType] = JStruct[AddressType]
    contact: Optional[ResponsiblePartyContactType] = JStruct[ResponsiblePartyContactType]


@s(auto_attribs=True)
class LabelSpecificationType:
    labelFormatType: Optional[str] = None
    labelOrder: Optional[str] = None
    customerSpecifiedDetail: Optional[CustomerSpecifiedDetailType] = JStruct[CustomerSpecifiedDetailType]
    printedLabelOrigin: Optional[OriginType] = JStruct[OriginType]
    labelStockType: Optional[str] = None
    labelRotation: Optional[str] = None
    imageType: Optional[str] = None
    labelPrintingOrientation: Optional[str] = None
    returnedDispositionDetail: Optional[bool] = None


@s(auto_attribs=True)
class MasterTrackingIDType:
    formId: Optional[str] = None
    trackingIdType: Optional[str] = None
    uspsApplicationId: Optional[int] = None
    trackingNumber: Optional[str] = None


@s(auto_attribs=True)
class ContentRecordType:
    itemNumber: Optional[int] = None
    receivedQuantity: Optional[int] = None
    description: Optional[str] = None
    partNumber: Optional[int] = None


@s(auto_attribs=True)
class DimensionsType:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class AlcoholDetailType:
    alcoholRecipientType: Optional[str] = None
    shipperAgreementType: Optional[str] = None


@s(auto_attribs=True)
class BatteryDetailType:
    batteryPackingType: Optional[str] = None
    batteryRegulatoryType: Optional[str] = None
    batteryMaterialType: Optional[str] = None


@s(auto_attribs=True)
class DangerousGoodsDetailType:
    cargoAircraftOnly: Optional[bool] = None
    accessibility: Optional[str] = None
    options: List[str] = []


@s(auto_attribs=True)
class PackageCODDetailType:
    codCollectionAmount: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]


@s(auto_attribs=True)
class PriorityAlertDetailType:
    enhancementTypes: List[str] = []
    content: List[str] = []


@s(auto_attribs=True)
class SignatureOptionDetailType:
    signatureReleaseNumber: Optional[int] = None


@s(auto_attribs=True)
class PackageSpecialServicesType:
    specialServiceTypes: List[str] = []
    signatureOptionType: Optional[str] = None
    priorityAlertDetail: Optional[PriorityAlertDetailType] = JStruct[PriorityAlertDetailType]
    signatureOptionDetail: Optional[SignatureOptionDetailType] = JStruct[SignatureOptionDetailType]
    alcoholDetail: Optional[AlcoholDetailType] = JStruct[AlcoholDetailType]
    dangerousGoodsDetail: Optional[DangerousGoodsDetailType] = JStruct[DangerousGoodsDetailType]
    packageCODDetail: Optional[PackageCODDetailType] = JStruct[PackageCODDetailType]
    pieceCountVerificationBoxCount: Optional[int] = None
    batteryDetails: List[BatteryDetailType] = JList[BatteryDetailType]
    dryIceWeight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class VariableHandlingChargeDetailType:
    rateType: Optional[str] = None
    percentValue: Optional[float] = None
    rateLevelType: Optional[str] = None
    fixedValue: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    rateElementBasis: Optional[str] = None


@s(auto_attribs=True)
class RequestedPackageLineItemType:
    sequenceNumber: Optional[int] = None
    subPackagingType: Optional[str] = None
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    declaredValue: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    weight: Optional[WeightType] = JStruct[WeightType]
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    groupPackageCount: Optional[int] = None
    itemDescriptionForClearance: Optional[str] = None
    contentRecord: List[ContentRecordType] = JList[ContentRecordType]
    itemDescription: Optional[str] = None
    variableHandlingChargeDetail: Optional[VariableHandlingChargeDetailType] = JStruct[VariableHandlingChargeDetailType]
    packageSpecialServices: Optional[PackageSpecialServicesType] = JStruct[PackageSpecialServicesType]
    trackingNumber: Optional[int] = None


@s(auto_attribs=True)
class DeliveryOnInvoiceAcceptanceDetailType:
    recipient: Optional[ShipperType] = JStruct[ShipperType]


@s(auto_attribs=True)
class AttachedDocumentType:
    documentType: Optional[str] = None
    documentReference: Optional[str] = None
    description: Optional[str] = None
    documentId: Optional[str] = None


@s(auto_attribs=True)
class EtdDetailType:
    attributes: List[str] = []
    attachedDocuments: List[AttachedDocumentType] = JList[AttachedDocumentType]
    requestedDocumentTypes: List[str] = []


@s(auto_attribs=True)
class HoldAtLocationDetailType:
    locationId: Optional[str] = None
    locationContactAndAddress: Optional[OriginType] = JStruct[OriginType]
    locationType: Optional[str] = None


@s(auto_attribs=True)
class PhoneNumberType:
    areaCode: Optional[int] = None
    localNumber: Optional[int] = None
    extension: Optional[int] = None
    personalIdentificationNumber: Optional[int] = None


@s(auto_attribs=True)
class HomeDeliveryPremiumDetailType:
    phoneNumber: Optional[PhoneNumberType] = JStruct[PhoneNumberType]
    deliveryDate: Optional[str] = None
    homedeliveryPremiumType: Optional[str] = None


@s(auto_attribs=True)
class InternationalControlledExportDetailType:
    licenseOrPermitExpirationDate: Optional[str] = None
    licenseOrPermitNumber: Optional[int] = None
    entryNumber: Optional[int] = None
    foreignTradeZoneCode: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class InternationalTrafficInArmsRegulationsDetailType:
    licenseOrExemptionNumber: Optional[int] = None


@s(auto_attribs=True)
class ProcessingOptionsType:
    options: List[str] = []


@s(auto_attribs=True)
class RecipientType:
    emailAddress: Optional[str] = None
    optionsRequested: Optional[ProcessingOptionsType] = JStruct[ProcessingOptionsType]
    role: Optional[str] = None
    locale: Optional[str] = None


@s(auto_attribs=True)
class EmailLabelDetailType:
    recipients: List[RecipientType] = JList[RecipientType]
    message: Optional[str] = None


@s(auto_attribs=True)
class RecommendedDocumentSpecificationType:
    types: Optional[str] = None


@s(auto_attribs=True)
class PendingShipmentDetailType:
    pendingShipmentType: Optional[str] = None
    processingOptions: Optional[ProcessingOptionsType] = JStruct[ProcessingOptionsType]
    recommendedDocumentSpecification: Optional[RecommendedDocumentSpecificationType] = JStruct[RecommendedDocumentSpecificationType]
    emailLabelDetail: Optional[EmailLabelDetailType] = JStruct[EmailLabelDetailType]
    attachedDocuments: List[AttachedDocumentType] = JList[AttachedDocumentType]
    expirationTimeStamp: Optional[str] = None


@s(auto_attribs=True)
class ReturnAssociationDetailType:
    shipDatestamp: Optional[str] = None
    trackingNumber: Optional[int] = None


@s(auto_attribs=True)
class ReturnEmailDetailType:
    merchantPhoneNumber: Optional[str] = None
    allowedSpecialService: List[str] = []


@s(auto_attribs=True)
class RmaType:
    reason: Optional[str] = None


@s(auto_attribs=True)
class ReturnShipmentDetailType:
    returnEmailDetail: Optional[ReturnEmailDetailType] = JStruct[ReturnEmailDetailType]
    rma: Optional[RmaType] = JStruct[RmaType]
    returnAssociationDetail: Optional[ReturnAssociationDetailType] = JStruct[ReturnAssociationDetailType]
    returnType: Optional[str] = None


@s(auto_attribs=True)
class AddTransportationChargesDetailType:
    rateType: Optional[str] = None
    rateLevelType: Optional[str] = None
    chargeLevelType: Optional[str] = None
    chargeType: Optional[str] = None


@s(auto_attribs=True)
class ShipmentCODDetailType:
    addTransportationChargesDetail: Optional[AddTransportationChargesDetailType] = JStruct[AddTransportationChargesDetailType]
    codRecipient: Optional[ShipperType] = JStruct[ShipperType]
    remitToName: Optional[str] = None
    codCollectionType: Optional[str] = None
    financialInstitutionContactAndAddress: Optional[OriginType] = JStruct[OriginType]
    codCollectionAmount: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    returnReferenceIndicatorType: Optional[str] = None
    shipmentCodAmount: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]


@s(auto_attribs=True)
class ShipmentDryIceDetailType:
    totalWeight: Optional[WeightType] = JStruct[WeightType]
    packageCount: Optional[int] = None


@s(auto_attribs=True)
class ShipmentSpecialServicesType:
    specialServiceTypes: List[str] = []
    etdDetail: Optional[EtdDetailType] = JStruct[EtdDetailType]
    returnShipmentDetail: Optional[ReturnShipmentDetailType] = JStruct[ReturnShipmentDetailType]
    deliveryOnInvoiceAcceptanceDetail: Optional[DeliveryOnInvoiceAcceptanceDetailType] = JStruct[DeliveryOnInvoiceAcceptanceDetailType]
    internationalTrafficInArmsRegulationsDetail: Optional[InternationalTrafficInArmsRegulationsDetailType] = JStruct[InternationalTrafficInArmsRegulationsDetailType]
    pendingShipmentDetail: Optional[PendingShipmentDetailType] = JStruct[PendingShipmentDetailType]
    holdAtLocationDetail: Optional[HoldAtLocationDetailType] = JStruct[HoldAtLocationDetailType]
    shipmentCODDetail: Optional[ShipmentCODDetailType] = JStruct[ShipmentCODDetailType]
    shipmentDryIceDetail: Optional[ShipmentDryIceDetailType] = JStruct[ShipmentDryIceDetailType]
    internationalControlledExportDetail: Optional[InternationalControlledExportDetailType] = JStruct[InternationalControlledExportDetailType]
    homeDeliveryPremiumDetail: Optional[HomeDeliveryPremiumDetailType] = JStruct[HomeDeliveryPremiumDetailType]


@s(auto_attribs=True)
class ShippingChargesPaymentType:
    paymentType: Optional[str] = None
    payor: Optional[PayorType] = JStruct[PayorType]


@s(auto_attribs=True)
class CustomerImageUsageType:
    id: Optional[str] = None
    type: Optional[str] = None
    providedImageType: Optional[str] = None


@s(auto_attribs=True)
class EMailRecipientType:
    emailAddress: Optional[str] = None
    recipientType: Optional[str] = None


@s(auto_attribs=True)
class EMailDetailType:
    eMailRecipients: List[EMailRecipientType] = JList[EMailRecipientType]
    locale: Optional[str] = None
    grouping: Optional[str] = None


@s(auto_attribs=True)
class DispositionType:
    eMailDetail: Optional[EMailDetailType] = JStruct[EMailDetailType]
    dispositionType: Optional[str] = None


@s(auto_attribs=True)
class DocumentFormatType:
    provideInstructions: Optional[bool] = None
    optionsRequested: Optional[ProcessingOptionsType] = JStruct[ProcessingOptionsType]
    stockType: Optional[str] = None
    dispositions: List[DispositionType] = JList[DispositionType]
    locale: Optional[str] = None
    docType: Optional[str] = None


@s(auto_attribs=True)
class CertificateOfOriginType:
    customerImageUsages: List[CustomerImageUsageType] = JList[CustomerImageUsageType]
    documentFormat: Optional[DocumentFormatType] = JStruct[DocumentFormatType]


@s(auto_attribs=True)
class GeneralAgencyAgreementDetailType:
    documentFormat: Optional[DocumentFormatType] = JStruct[DocumentFormatType]


@s(auto_attribs=True)
class Op900DetailType:
    customerImageUsages: List[CustomerImageUsageType] = JList[CustomerImageUsageType]
    signatureName: Optional[str] = None
    documentFormat: Optional[DocumentFormatType] = JStruct[DocumentFormatType]


@s(auto_attribs=True)
class ReturnInstructionsDetailType:
    customText: Optional[str] = None
    documentFormat: Optional[DocumentFormatType] = JStruct[DocumentFormatType]


@s(auto_attribs=True)
class BlanketPeriodType:
    begins: Optional[str] = None
    ends: Optional[str] = None


@s(auto_attribs=True)
class UsmcaCCertificationOfOriginDetailType:
    customerImageUsages: List[CustomerImageUsageType] = JList[CustomerImageUsageType]
    documentFormat: Optional[DocumentFormatType] = JStruct[DocumentFormatType]
    certifierSpecification: Optional[str] = None
    importerSpecification: Optional[str] = None
    producerSpecification: Optional[str] = None
    producer: Optional[ShipperType] = JStruct[ShipperType]
    blanketPeriod: Optional[BlanketPeriodType] = JStruct[BlanketPeriodType]
    certifierJobTitle: Optional[str] = None


@s(auto_attribs=True)
class ShippingDocumentSpecificationType:
    generalAgencyAgreementDetail: Optional[GeneralAgencyAgreementDetailType] = JStruct[GeneralAgencyAgreementDetailType]
    returnInstructionsDetail: Optional[ReturnInstructionsDetailType] = JStruct[ReturnInstructionsDetailType]
    op900Detail: Optional[Op900DetailType] = JStruct[Op900DetailType]
    usmcaCertificationOfOriginDetail: Optional[UsmcaCCertificationOfOriginDetailType] = JStruct[UsmcaCCertificationOfOriginDetailType]
    usmcaCommercialInvoiceCertificationOfOriginDetail: Optional[UsmcaCCertificationOfOriginDetailType] = JStruct[UsmcaCCertificationOfOriginDetailType]
    shippingDocumentTypes: List[str] = []
    certificateOfOrigin: Optional[CertificateOfOriginType] = JStruct[CertificateOfOriginType]
    commercialInvoiceDetail: Optional[CertificateOfOriginType] = JStruct[CertificateOfOriginType]


@s(auto_attribs=True)
class SmartPostInfoDetailType:
    ancillaryEndorsement: Optional[str] = None
    hubId: Optional[int] = None
    indicia: Optional[str] = None
    specialServices: Optional[str] = None


@s(auto_attribs=True)
class RequestedShipmentType:
    shipDatestamp: Optional[str] = None
    totalDeclaredValue: Optional[TotalDeclaredValueType] = JStruct[TotalDeclaredValueType]
    shipper: Optional[ShipperType] = JStruct[ShipperType]
    soldTo: Optional[ShipperType] = JStruct[ShipperType]
    recipients: List[ShipperType] = JList[ShipperType]
    recipientLocationNumber: Optional[int] = None
    pickupType: Optional[str] = None
    serviceType: Optional[str] = None
    packagingType: Optional[str] = None
    totalWeight: Optional[float] = None
    origin: Optional[OriginType] = JStruct[OriginType]
    shippingChargesPayment: Optional[ShippingChargesPaymentType] = JStruct[ShippingChargesPaymentType]
    shipmentSpecialServices: Optional[ShipmentSpecialServicesType] = JStruct[ShipmentSpecialServicesType]
    emailNotificationDetail: Optional[RequestedShipmentEmailNotificationDetailType] = JStruct[RequestedShipmentEmailNotificationDetailType]
    expressFreightDetail: Optional[ExpressFreightDetailType] = JStruct[ExpressFreightDetailType]
    variableHandlingChargeDetail: Optional[VariableHandlingChargeDetailType] = JStruct[VariableHandlingChargeDetailType]
    customsClearanceDetail: Optional[CustomsClearanceDetailType] = JStruct[CustomsClearanceDetailType]
    smartPostInfoDetail: Optional[SmartPostInfoDetailType] = JStruct[SmartPostInfoDetailType]
    blockInsightVisibility: Optional[bool] = None
    labelSpecification: Optional[LabelSpecificationType] = JStruct[LabelSpecificationType]
    shippingDocumentSpecification: Optional[ShippingDocumentSpecificationType] = JStruct[ShippingDocumentSpecificationType]
    rateRequestType: List[str] = []
    preferredCurrency: Optional[str] = None
    totalPackageCount: Optional[int] = None
    masterTrackingId: Optional[MasterTrackingIDType] = JStruct[MasterTrackingIDType]
    requestedPackageLineItems: List[RequestedPackageLineItemType] = JList[RequestedPackageLineItemType]


@s(auto_attribs=True)
class ShippingRequestType:
    mergeLabelDocOption: Optional[str] = None
    requestedShipment: Optional[RequestedShipmentType] = JStruct[RequestedShipmentType]
    labelResponseOptions: Optional[str] = None
    accountNumber: Optional[AccountNumberType] = JStruct[AccountNumberType]
    shipAction: Optional[str] = None
    processingOptionType: Optional[str] = None
    oneLabelAtATime: Optional[bool] = None
