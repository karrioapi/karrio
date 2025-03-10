import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountNumberType:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    streetLines: typing.Optional[typing.List[str]] = None
    city: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    countryCode: typing.Optional[str] = None
    residential: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class BrokerContactType:
    personName: typing.Optional[str] = None
    emailAddress: typing.Optional[str] = None
    phoneNumber: typing.Optional[int] = None
    phoneExtension: typing.Optional[int] = None
    companyName: typing.Optional[str] = None
    faxNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class TinType:
    number: typing.Optional[str] = None
    tinType: typing.Optional[str] = None
    usage: typing.Optional[str] = None
    effectiveDate: typing.Optional[str] = None
    expirationDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BrokerBrokerType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[BrokerContactType] = jstruct.JStruct[BrokerContactType]
    accountNumber: typing.Optional[AccountNumberType] = jstruct.JStruct[AccountNumberType]
    tins: typing.Optional[typing.List[TinType]] = jstruct.JList[TinType]
    deliveryInstructions: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BrokerElementType:
    broker: typing.Optional[BrokerBrokerType] = jstruct.JStruct[BrokerBrokerType]
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerReferenceType:
    customerReferenceType: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CommercialInvoiceEmailNotificationDetailType:
    emailAddress: typing.Optional[str] = None
    type: typing.Optional[str] = None
    recipientType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TotalDeclaredValueType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommercialInvoiceType:
    originatorName: typing.Optional[str] = None
    comments: typing.Optional[typing.List[str]] = None
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    taxesOrMiscellaneousCharge: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    taxesOrMiscellaneousChargeType: typing.Optional[str] = None
    freightCharge: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    packingCosts: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    handlingCosts: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    declarationStatement: typing.Optional[str] = None
    termsOfSale: typing.Optional[str] = None
    specialInstructions: typing.Optional[str] = None
    shipmentPurpose: typing.Optional[str] = None
    emailNotificationDetail: typing.Optional[CommercialInvoiceEmailNotificationDetailType] = jstruct.JStruct[CommercialInvoiceEmailNotificationDetailType]


@attr.s(auto_attribs=True)
class AdditionalMeasureType:
    quantity: typing.Optional[float] = None
    units: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsValueType:
    amount: typing.Optional[str] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UsmcaDetailType:
    originCriterion: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    units: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class CommodityType:
    unitPrice: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    additionalMeasures: typing.Optional[typing.List[AdditionalMeasureType]] = jstruct.JList[AdditionalMeasureType]
    numberOfPieces: typing.Optional[int] = None
    quantity: typing.Optional[int] = None
    quantityUnits: typing.Optional[str] = None
    customsValue: typing.Optional[CustomsValueType] = jstruct.JStruct[CustomsValueType]
    countryOfManufacture: typing.Optional[str] = None
    cIMarksAndNumbers: typing.Optional[int] = None
    harmonizedCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    name: typing.Optional[str] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    exportLicenseNumber: typing.Optional[int] = None
    exportLicenseExpirationDate: typing.Optional[str] = None
    partNumber: typing.Optional[int] = None
    purpose: typing.Optional[str] = None
    usmcaDetail: typing.Optional[UsmcaDetailType] = jstruct.JStruct[UsmcaDetailType]


@attr.s(auto_attribs=True)
class CustomsOptionType:
    description: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UsmcaLowValueStatementDetailType:
    countryOfOriginLowValueDocumentRequested: typing.Optional[bool] = None
    customsRole: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeclarationStatementDetailType:
    usmcaLowValueStatementDetail: typing.Optional[UsmcaLowValueStatementDetailType] = jstruct.JStruct[UsmcaLowValueStatementDetailType]


@attr.s(auto_attribs=True)
class BillingDetailsType:
    billingCode: typing.Optional[str] = None
    billingType: typing.Optional[str] = None
    aliasId: typing.Optional[str] = None
    accountNickname: typing.Optional[str] = None
    accountNumber: typing.Optional[str] = None
    accountNumberCountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponsiblePartyContactType:
    personName: typing.Optional[str] = None
    emailAddress: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    phoneExtension: typing.Optional[str] = None
    companyName: typing.Optional[str] = None
    faxNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponsiblePartyType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[ResponsiblePartyContactType] = jstruct.JStruct[ResponsiblePartyContactType]
    accountNumber: typing.Optional[AccountNumberType] = jstruct.JStruct[AccountNumberType]
    tins: typing.Optional[typing.List[TinType]] = jstruct.JList[TinType]


@attr.s(auto_attribs=True)
class PayorType:
    responsibleParty: typing.Optional[ResponsiblePartyType] = jstruct.JStruct[ResponsiblePartyType]


@attr.s(auto_attribs=True)
class DutiesPaymentType:
    payor: typing.Optional[PayorType] = jstruct.JStruct[PayorType]
    billingDetails: typing.Optional[BillingDetailsType] = jstruct.JStruct[BillingDetailsType]
    paymentType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DestinationControlDetailType:
    endUser: typing.Optional[str] = None
    statementTypes: typing.Optional[str] = None
    destinationCountries: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ExportDetailType:
    destinationControlDetail: typing.Optional[DestinationControlDetailType] = jstruct.JStruct[DestinationControlDetailType]
    b13AFilingOption: typing.Optional[str] = None
    exportComplianceStatement: typing.Optional[str] = None
    permitNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipperType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[ResponsiblePartyContactType] = jstruct.JStruct[ResponsiblePartyContactType]
    accountNumber: typing.Optional[AccountNumberType] = jstruct.JStruct[AccountNumberType]
    tins: typing.Optional[typing.List[TinType]] = jstruct.JList[TinType]
    deliveryInstructions: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RecipientCustomsIDType:
    type: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CustomsClearanceDetailType:
    regulatoryControls: typing.Optional[str] = None
    brokers: typing.Optional[typing.List[BrokerElementType]] = jstruct.JList[BrokerElementType]
    commercialInvoice: typing.Optional[CommercialInvoiceType] = jstruct.JStruct[CommercialInvoiceType]
    freightOnValue: typing.Optional[str] = None
    dutiesPayment: typing.Optional[DutiesPaymentType] = jstruct.JStruct[DutiesPaymentType]
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    isDocumentOnly: typing.Optional[bool] = None
    recipientCustomsId: typing.Optional[RecipientCustomsIDType] = jstruct.JStruct[RecipientCustomsIDType]
    customsOption: typing.Optional[CustomsOptionType] = jstruct.JStruct[CustomsOptionType]
    importerOfRecord: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    generatedDocumentLocale: typing.Optional[str] = None
    exportDetail: typing.Optional[ExportDetailType] = jstruct.JStruct[ExportDetailType]
    totalCustomsValue: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    partiesToTransactionAreRelated: typing.Optional[bool] = None
    declarationStatementDetail: typing.Optional[DeclarationStatementDetailType] = jstruct.JStruct[DeclarationStatementDetailType]
    insuranceCharge: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]


@attr.s(auto_attribs=True)
class EmailNotificationRecipientType:
    name: typing.Optional[str] = None
    emailNotificationRecipientType: typing.Optional[str] = None
    emailAddress: typing.Optional[str] = None
    notificationFormatType: typing.Optional[str] = None
    notificationType: typing.Optional[str] = None
    locale: typing.Optional[str] = None
    notificationEventType: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class RequestedShipmentEmailNotificationDetailType:
    aggregationType: typing.Optional[str] = None
    emailNotificationRecipients: typing.Optional[typing.List[EmailNotificationRecipientType]] = jstruct.JList[EmailNotificationRecipientType]
    personalMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExpressFreightDetailType:
    bookingConfirmationNumber: typing.Optional[str] = None
    shippersLoadAndCount: typing.Optional[int] = None
    packingListEnclosed: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class AdditionalLabelType:
    type: typing.Optional[str] = None
    count: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class SpecificationType:
    zoneNumber: typing.Optional[int] = None
    header: typing.Optional[str] = None
    dataField: typing.Optional[str] = None
    literalValue: typing.Optional[str] = None
    justification: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BarcodedType:
    symbology: typing.Optional[str] = None
    specification: typing.Optional[SpecificationType] = jstruct.JStruct[SpecificationType]


@attr.s(auto_attribs=True)
class Zone001Type:
    docTabZoneSpecifications: typing.Optional[typing.List[SpecificationType]] = jstruct.JList[SpecificationType]


@attr.s(auto_attribs=True)
class DocTabContentType:
    docTabContentType: typing.Optional[str] = None
    zone001: typing.Optional[Zone001Type] = jstruct.JStruct[Zone001Type]
    barcoded: typing.Optional[BarcodedType] = jstruct.JStruct[BarcodedType]


@attr.s(auto_attribs=True)
class RegulatoryLabelType:
    generationOptions: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerSpecifiedDetailType:
    maskedData: typing.Optional[typing.List[str]] = None
    regulatoryLabels: typing.Optional[typing.List[RegulatoryLabelType]] = jstruct.JList[RegulatoryLabelType]
    additionalLabels: typing.Optional[typing.List[AdditionalLabelType]] = jstruct.JList[AdditionalLabelType]
    docTabContent: typing.Optional[DocTabContentType] = jstruct.JStruct[DocTabContentType]


@attr.s(auto_attribs=True)
class OriginType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[ResponsiblePartyContactType] = jstruct.JStruct[ResponsiblePartyContactType]


@attr.s(auto_attribs=True)
class LabelSpecificationType:
    labelFormatType: typing.Optional[str] = None
    labelOrder: typing.Optional[str] = None
    customerSpecifiedDetail: typing.Optional[CustomerSpecifiedDetailType] = jstruct.JStruct[CustomerSpecifiedDetailType]
    printedLabelOrigin: typing.Optional[OriginType] = jstruct.JStruct[OriginType]
    labelStockType: typing.Optional[str] = None
    labelRotation: typing.Optional[str] = None
    imageType: typing.Optional[str] = None
    labelPrintingOrientation: typing.Optional[str] = None
    returnedDispositionDetail: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class MasterTrackingIDType:
    formId: typing.Optional[str] = None
    trackingIdType: typing.Optional[str] = None
    uspsApplicationId: typing.Optional[int] = None
    trackingNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContentRecordType:
    itemNumber: typing.Optional[int] = None
    receivedQuantity: typing.Optional[int] = None
    description: typing.Optional[str] = None
    partNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    units: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AlcoholDetailType:
    alcoholRecipientType: typing.Optional[str] = None
    shipperAgreementType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BatteryDetailType:
    batteryPackingType: typing.Optional[str] = None
    batteryRegulatoryType: typing.Optional[str] = None
    batteryMaterialType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DangerousGoodsDetailType:
    cargoAircraftOnly: typing.Optional[bool] = None
    accessibility: typing.Optional[str] = None
    options: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class PackageCODDetailType:
    codCollectionAmount: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]


@attr.s(auto_attribs=True)
class PriorityAlertDetailType:
    enhancementTypes: typing.Optional[typing.List[str]] = None
    content: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class SignatureOptionDetailType:
    signatureReleaseNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackageSpecialServicesType:
    specialServiceTypes: typing.Optional[typing.List[str]] = None
    signatureOptionType: typing.Optional[str] = None
    priorityAlertDetail: typing.Optional[PriorityAlertDetailType] = jstruct.JStruct[PriorityAlertDetailType]
    signatureOptionDetail: typing.Optional[SignatureOptionDetailType] = jstruct.JStruct[SignatureOptionDetailType]
    alcoholDetail: typing.Optional[AlcoholDetailType] = jstruct.JStruct[AlcoholDetailType]
    dangerousGoodsDetail: typing.Optional[DangerousGoodsDetailType] = jstruct.JStruct[DangerousGoodsDetailType]
    packageCODDetail: typing.Optional[PackageCODDetailType] = jstruct.JStruct[PackageCODDetailType]
    pieceCountVerificationBoxCount: typing.Optional[int] = None
    batteryDetails: typing.Optional[typing.List[BatteryDetailType]] = jstruct.JList[BatteryDetailType]
    dryIceWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class VariableHandlingChargeDetailType:
    rateType: typing.Optional[str] = None
    percentValue: typing.Optional[float] = None
    rateLevelType: typing.Optional[str] = None
    fixedValue: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    rateElementBasis: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestedPackageLineItemType:
    sequenceNumber: typing.Optional[int] = None
    subPackagingType: typing.Optional[str] = None
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    declaredValue: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    groupPackageCount: typing.Optional[int] = None
    itemDescriptionForClearance: typing.Optional[str] = None
    contentRecord: typing.Optional[typing.List[ContentRecordType]] = jstruct.JList[ContentRecordType]
    itemDescription: typing.Optional[str] = None
    variableHandlingChargeDetail: typing.Optional[VariableHandlingChargeDetailType] = jstruct.JStruct[VariableHandlingChargeDetailType]
    packageSpecialServices: typing.Optional[PackageSpecialServicesType] = jstruct.JStruct[PackageSpecialServicesType]
    trackingNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DeliveryOnInvoiceAcceptanceDetailType:
    recipient: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]


@attr.s(auto_attribs=True)
class AttachedDocumentType:
    documentType: typing.Optional[str] = None
    documentReference: typing.Optional[str] = None
    description: typing.Optional[str] = None
    documentId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EtdDetailType:
    attributes: typing.Optional[typing.List[str]] = None
    attachedDocuments: typing.Optional[typing.List[AttachedDocumentType]] = jstruct.JList[AttachedDocumentType]
    requestedDocumentTypes: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class HoldAtLocationDetailType:
    locationId: typing.Optional[str] = None
    locationContactAndAddress: typing.Optional[OriginType] = jstruct.JStruct[OriginType]
    locationType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PhoneNumberType:
    areaCode: typing.Optional[int] = None
    localNumber: typing.Optional[int] = None
    extension: typing.Optional[int] = None
    personalIdentificationNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class HomeDeliveryPremiumDetailType:
    phoneNumber: typing.Optional[PhoneNumberType] = jstruct.JStruct[PhoneNumberType]
    deliveryDate: typing.Optional[str] = None
    homedeliveryPremiumType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalControlledExportDetailType:
    licenseOrPermitExpirationDate: typing.Optional[str] = None
    licenseOrPermitNumber: typing.Optional[int] = None
    entryNumber: typing.Optional[int] = None
    foreignTradeZoneCode: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalTrafficInArmsRegulationsDetailType:
    licenseOrExemptionNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ProcessingOptionsType:
    options: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class RecipientType:
    emailAddress: typing.Optional[str] = None
    optionsRequested: typing.Optional[ProcessingOptionsType] = jstruct.JStruct[ProcessingOptionsType]
    role: typing.Optional[str] = None
    locale: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EmailLabelDetailType:
    recipients: typing.Optional[typing.List[RecipientType]] = jstruct.JList[RecipientType]
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RecommendedDocumentSpecificationType:
    types: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PendingShipmentDetailType:
    pendingShipmentType: typing.Optional[str] = None
    processingOptions: typing.Optional[ProcessingOptionsType] = jstruct.JStruct[ProcessingOptionsType]
    recommendedDocumentSpecification: typing.Optional[RecommendedDocumentSpecificationType] = jstruct.JStruct[RecommendedDocumentSpecificationType]
    emailLabelDetail: typing.Optional[EmailLabelDetailType] = jstruct.JStruct[EmailLabelDetailType]
    attachedDocuments: typing.Optional[typing.List[AttachedDocumentType]] = jstruct.JList[AttachedDocumentType]
    expirationTimeStamp: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReturnAssociationDetailType:
    shipDatestamp: typing.Optional[str] = None
    trackingNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ReturnEmailDetailType:
    merchantPhoneNumber: typing.Optional[str] = None
    allowedSpecialService: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class RmaType:
    reason: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReturnShipmentDetailType:
    returnEmailDetail: typing.Optional[ReturnEmailDetailType] = jstruct.JStruct[ReturnEmailDetailType]
    rma: typing.Optional[RmaType] = jstruct.JStruct[RmaType]
    returnAssociationDetail: typing.Optional[ReturnAssociationDetailType] = jstruct.JStruct[ReturnAssociationDetailType]
    returnType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddTransportationChargesDetailType:
    rateType: typing.Optional[str] = None
    rateLevelType: typing.Optional[str] = None
    chargeLevelType: typing.Optional[str] = None
    chargeType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentCODDetailType:
    addTransportationChargesDetail: typing.Optional[AddTransportationChargesDetailType] = jstruct.JStruct[AddTransportationChargesDetailType]
    codRecipient: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    remitToName: typing.Optional[str] = None
    codCollectionType: typing.Optional[str] = None
    financialInstitutionContactAndAddress: typing.Optional[OriginType] = jstruct.JStruct[OriginType]
    codCollectionAmount: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    returnReferenceIndicatorType: typing.Optional[str] = None
    shipmentCodAmount: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]


@attr.s(auto_attribs=True)
class ShipmentDryIceDetailType:
    totalWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    packageCount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipmentSpecialServicesType:
    specialServiceTypes: typing.Optional[typing.List[str]] = None
    etdDetail: typing.Optional[EtdDetailType] = jstruct.JStruct[EtdDetailType]
    returnShipmentDetail: typing.Optional[ReturnShipmentDetailType] = jstruct.JStruct[ReturnShipmentDetailType]
    deliveryOnInvoiceAcceptanceDetail: typing.Optional[DeliveryOnInvoiceAcceptanceDetailType] = jstruct.JStruct[DeliveryOnInvoiceAcceptanceDetailType]
    internationalTrafficInArmsRegulationsDetail: typing.Optional[InternationalTrafficInArmsRegulationsDetailType] = jstruct.JStruct[InternationalTrafficInArmsRegulationsDetailType]
    pendingShipmentDetail: typing.Optional[PendingShipmentDetailType] = jstruct.JStruct[PendingShipmentDetailType]
    holdAtLocationDetail: typing.Optional[HoldAtLocationDetailType] = jstruct.JStruct[HoldAtLocationDetailType]
    shipmentCODDetail: typing.Optional[ShipmentCODDetailType] = jstruct.JStruct[ShipmentCODDetailType]
    shipmentDryIceDetail: typing.Optional[ShipmentDryIceDetailType] = jstruct.JStruct[ShipmentDryIceDetailType]
    internationalControlledExportDetail: typing.Optional[InternationalControlledExportDetailType] = jstruct.JStruct[InternationalControlledExportDetailType]
    homeDeliveryPremiumDetail: typing.Optional[HomeDeliveryPremiumDetailType] = jstruct.JStruct[HomeDeliveryPremiumDetailType]


@attr.s(auto_attribs=True)
class ShippingChargesPaymentType:
    paymentType: typing.Optional[str] = None
    payor: typing.Optional[PayorType] = jstruct.JStruct[PayorType]


@attr.s(auto_attribs=True)
class CustomerImageUsageType:
    id: typing.Optional[str] = None
    type: typing.Optional[str] = None
    providedImageType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EMailRecipientType:
    emailAddress: typing.Optional[str] = None
    recipientType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EMailDetailType:
    eMailRecipients: typing.Optional[typing.List[EMailRecipientType]] = jstruct.JList[EMailRecipientType]
    locale: typing.Optional[str] = None
    grouping: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DispositionType:
    eMailDetail: typing.Optional[EMailDetailType] = jstruct.JStruct[EMailDetailType]
    dispositionType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DocumentFormatType:
    provideInstructions: typing.Optional[bool] = None
    optionsRequested: typing.Optional[ProcessingOptionsType] = jstruct.JStruct[ProcessingOptionsType]
    stockType: typing.Optional[str] = None
    dispositions: typing.Optional[typing.List[DispositionType]] = jstruct.JList[DispositionType]
    locale: typing.Optional[str] = None
    docType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CertificateOfOriginType:
    customerImageUsages: typing.Optional[typing.List[CustomerImageUsageType]] = jstruct.JList[CustomerImageUsageType]
    documentFormat: typing.Optional[DocumentFormatType] = jstruct.JStruct[DocumentFormatType]


@attr.s(auto_attribs=True)
class GeneralAgencyAgreementDetailType:
    documentFormat: typing.Optional[DocumentFormatType] = jstruct.JStruct[DocumentFormatType]


@attr.s(auto_attribs=True)
class Op900DetailType:
    customerImageUsages: typing.Optional[typing.List[CustomerImageUsageType]] = jstruct.JList[CustomerImageUsageType]
    signatureName: typing.Optional[str] = None
    documentFormat: typing.Optional[DocumentFormatType] = jstruct.JStruct[DocumentFormatType]


@attr.s(auto_attribs=True)
class ReturnInstructionsDetailType:
    customText: typing.Optional[str] = None
    documentFormat: typing.Optional[DocumentFormatType] = jstruct.JStruct[DocumentFormatType]


@attr.s(auto_attribs=True)
class BlanketPeriodType:
    begins: typing.Optional[str] = None
    ends: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UsmcaCCertificationOfOriginDetailType:
    customerImageUsages: typing.Optional[typing.List[CustomerImageUsageType]] = jstruct.JList[CustomerImageUsageType]
    documentFormat: typing.Optional[DocumentFormatType] = jstruct.JStruct[DocumentFormatType]
    certifierSpecification: typing.Optional[str] = None
    importerSpecification: typing.Optional[str] = None
    producerSpecification: typing.Optional[str] = None
    producer: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    blanketPeriod: typing.Optional[BlanketPeriodType] = jstruct.JStruct[BlanketPeriodType]
    certifierJobTitle: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingDocumentSpecificationType:
    generalAgencyAgreementDetail: typing.Optional[GeneralAgencyAgreementDetailType] = jstruct.JStruct[GeneralAgencyAgreementDetailType]
    returnInstructionsDetail: typing.Optional[ReturnInstructionsDetailType] = jstruct.JStruct[ReturnInstructionsDetailType]
    op900Detail: typing.Optional[Op900DetailType] = jstruct.JStruct[Op900DetailType]
    usmcaCertificationOfOriginDetail: typing.Optional[UsmcaCCertificationOfOriginDetailType] = jstruct.JStruct[UsmcaCCertificationOfOriginDetailType]
    usmcaCommercialInvoiceCertificationOfOriginDetail: typing.Optional[UsmcaCCertificationOfOriginDetailType] = jstruct.JStruct[UsmcaCCertificationOfOriginDetailType]
    shippingDocumentTypes: typing.Optional[typing.List[str]] = None
    certificateOfOrigin: typing.Optional[CertificateOfOriginType] = jstruct.JStruct[CertificateOfOriginType]
    commercialInvoiceDetail: typing.Optional[CertificateOfOriginType] = jstruct.JStruct[CertificateOfOriginType]


@attr.s(auto_attribs=True)
class SmartPostInfoDetailType:
    ancillaryEndorsement: typing.Optional[str] = None
    hubId: typing.Optional[int] = None
    indicia: typing.Optional[str] = None
    specialServices: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestedShipmentType:
    shipDatestamp: typing.Optional[str] = None
    totalDeclaredValue: typing.Optional[TotalDeclaredValueType] = jstruct.JStruct[TotalDeclaredValueType]
    shipper: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    soldTo: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    recipients: typing.Optional[typing.List[ShipperType]] = jstruct.JList[ShipperType]
    recipientLocationNumber: typing.Optional[int] = None
    pickupType: typing.Optional[str] = None
    serviceType: typing.Optional[str] = None
    packagingType: typing.Optional[str] = None
    totalWeight: typing.Optional[float] = None
    origin: typing.Optional[OriginType] = jstruct.JStruct[OriginType]
    shippingChargesPayment: typing.Optional[ShippingChargesPaymentType] = jstruct.JStruct[ShippingChargesPaymentType]
    shipmentSpecialServices: typing.Optional[ShipmentSpecialServicesType] = jstruct.JStruct[ShipmentSpecialServicesType]
    emailNotificationDetail: typing.Optional[RequestedShipmentEmailNotificationDetailType] = jstruct.JStruct[RequestedShipmentEmailNotificationDetailType]
    expressFreightDetail: typing.Optional[ExpressFreightDetailType] = jstruct.JStruct[ExpressFreightDetailType]
    variableHandlingChargeDetail: typing.Optional[VariableHandlingChargeDetailType] = jstruct.JStruct[VariableHandlingChargeDetailType]
    customsClearanceDetail: typing.Optional[CustomsClearanceDetailType] = jstruct.JStruct[CustomsClearanceDetailType]
    smartPostInfoDetail: typing.Optional[SmartPostInfoDetailType] = jstruct.JStruct[SmartPostInfoDetailType]
    blockInsightVisibility: typing.Optional[bool] = None
    labelSpecification: typing.Optional[LabelSpecificationType] = jstruct.JStruct[LabelSpecificationType]
    shippingDocumentSpecification: typing.Optional[ShippingDocumentSpecificationType] = jstruct.JStruct[ShippingDocumentSpecificationType]
    rateRequestType: typing.Optional[typing.List[str]] = None
    preferredCurrency: typing.Optional[str] = None
    totalPackageCount: typing.Optional[int] = None
    masterTrackingId: typing.Optional[MasterTrackingIDType] = jstruct.JStruct[MasterTrackingIDType]
    requestedPackageLineItems: typing.Optional[typing.List[RequestedPackageLineItemType]] = jstruct.JList[RequestedPackageLineItemType]


@attr.s(auto_attribs=True)
class ShippingRequestType:
    mergeLabelDocOption: typing.Optional[str] = None
    requestedShipment: typing.Optional[RequestedShipmentType] = jstruct.JStruct[RequestedShipmentType]
    labelResponseOptions: typing.Optional[str] = None
    accountNumber: typing.Optional[AccountNumberType] = jstruct.JStruct[AccountNumberType]
    shipAction: typing.Optional[str] = None
    processingOptionType: typing.Optional[str] = None
    oneLabelAtATime: typing.Optional[bool] = None
