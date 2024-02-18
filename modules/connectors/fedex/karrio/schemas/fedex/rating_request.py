from attr import s
from typing import Optional, List, Any
from jstruct import JStruct, JList


@s(auto_attribs=True)
class RatingRequestAccountNumberType:
    value: Optional[str] = None


@s(auto_attribs=True)
class RateRequestControlParametersType:
    returnTransitTimes: Optional[bool] = None
    servicesNeededOnRateFailure: Optional[bool] = None
    variableOptions: Optional[str] = None
    rateSortOrder: Optional[str] = None


@s(auto_attribs=True)
class RecipientAccountNumberType:
    value: Optional[int] = None


@s(auto_attribs=True)
class BrokerAddressType:
    streetLines: List[str] = []
    countryCode: Optional[str] = None


@s(auto_attribs=True)
class RecipientContactType:
    companyName: Optional[str] = None
    faxNumber: Optional[str] = None
    personName: Optional[str] = None
    phoneNumber: Optional[str] = None


@s(auto_attribs=True)
class BrokerClassType:
    accountNumber: Optional[RecipientAccountNumberType] = JStruct[RecipientAccountNumberType]
    address: Optional[BrokerAddressType] = JStruct[BrokerAddressType]
    contact: Optional[RecipientContactType] = JStruct[RecipientContactType]


@s(auto_attribs=True)
class BrokerAddressClassType:
    streetLines: List[str] = []
    city: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    postalCode: Optional[int] = None
    countryCode: Optional[str] = None
    residential: Optional[bool] = None
    classification: Optional[str] = None
    geographicCoordinates: Optional[str] = None
    urbanizationCode: Optional[str] = None
    countryName: Optional[str] = None


@s(auto_attribs=True)
class BrokerType:
    broker: Optional[BrokerClassType] = JStruct[BrokerClassType]
    type: Optional[str] = None
    brokerCommitTimestamp: Optional[str] = None
    brokerCommitDayOfWeek: Optional[str] = None
    brokerLocationId: Optional[str] = None
    brokerAddress: Optional[BrokerAddressClassType] = JStruct[BrokerAddressClassType]
    brokerToDestinationDays: Optional[int] = None


@s(auto_attribs=True)
class CommercialInvoiceType:
    shipmentPurpose: Optional[str] = None


@s(auto_attribs=True)
class FixedValueType:
    amount: Optional[int] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    units: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class CommodityType:
    description: Optional[str] = None
    weight: Optional[WeightType] = JStruct[WeightType]
    quantity: Optional[int] = None
    customsValue: Optional[FixedValueType] = JStruct[FixedValueType]
    unitPrice: Optional[FixedValueType] = JStruct[FixedValueType]
    numberOfPieces: Optional[int] = None
    countryOfManufacture: Optional[str] = None
    quantityUnits: Optional[str] = None
    name: Optional[str] = None
    harmonizedCode: Optional[str] = None
    partNumber: Optional[str] = None


@s(auto_attribs=True)
class ResponsiblePartyAddressType:
    streetLines: List[str] = []
    city: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    postalCode: Optional[int] = None
    countryCode: Optional[str] = None
    residential: Optional[bool] = None


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
    address: Optional[ResponsiblePartyAddressType] = JStruct[ResponsiblePartyAddressType]
    contact: Optional[ResponsiblePartyContactType] = JStruct[ResponsiblePartyContactType]
    accountNumber: Optional[RatingRequestAccountNumberType] = JStruct[RatingRequestAccountNumberType]


@s(auto_attribs=True)
class PayorType:
    responsibleParty: Optional[ResponsiblePartyType] = JStruct[ResponsiblePartyType]


@s(auto_attribs=True)
class DutiesPaymentType:
    payor: Optional[PayorType] = JStruct[PayorType]
    paymentType: Optional[str] = None


@s(auto_attribs=True)
class CustomsClearanceDetailType:
    brokers: List[BrokerType] = JList[BrokerType]
    commercialInvoice: Optional[CommercialInvoiceType] = JStruct[CommercialInvoiceType]
    freightOnValue: Optional[str] = None
    dutiesPayment: Optional[DutiesPaymentType] = JStruct[DutiesPaymentType]
    commodities: List[CommodityType] = JList[CommodityType]


@s(auto_attribs=True)
class PrintedReferenceType:
    printedReferenceType: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class EmailNotificationDetailRecipientType:
    emailAddress: Optional[str] = None
    notificationEventType: List[str] = []
    smsDetail: Any = None
    notificationFormatType: Optional[str] = None
    emailNotificationRecipientType: Optional[str] = None
    notificationType: Optional[str] = None
    locale: Optional[str] = None


@s(auto_attribs=True)
class EmailNotificationDetailType:
    recipients: List[EmailNotificationDetailRecipientType] = JList[EmailNotificationDetailRecipientType]
    personalMessage: Optional[str] = None
    PrintedReference: Optional[PrintedReferenceType] = JStruct[PrintedReferenceType]


@s(auto_attribs=True)
class ExpressFreightDetailType:
    bookingConfirmationNumber: Optional[str] = None
    shippersLoadAndCount: Optional[int] = None


@s(auto_attribs=True)
class ShipperClassType:
    address: Optional[ResponsiblePartyAddressType] = JStruct[ResponsiblePartyAddressType]


@s(auto_attribs=True)
class ContentRecordType:
    itemNumber: Optional[str] = None
    receivedQuantity: Optional[int] = None
    description: Optional[str] = None
    partNumber: Optional[str] = None


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
    material: Optional[str] = None
    regulatorySubType: Optional[str] = None
    packing: Optional[str] = None


@s(auto_attribs=True)
class NumberType:
    areaCode: Optional[str] = None
    extension: Optional[str] = None
    countryCode: Optional[str] = None
    personalIdentificationNumber: Optional[str] = None
    localNumber: Optional[str] = None


@s(auto_attribs=True)
class HazardousCommodityType:
    innerReceptacles: List[Any] = []


@s(auto_attribs=True)
class PackagingType:
    count: Optional[int] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class ContainerType:
    offeror: Optional[str] = None
    hazardousCommodities: List[HazardousCommodityType] = JList[HazardousCommodityType]
    numberOfContainers: Optional[int] = None
    containerType: Optional[str] = None
    emergencyContactNumber: Optional[NumberType] = JStruct[NumberType]
    packaging: Optional[PackagingType] = JStruct[PackagingType]
    packingType: Optional[str] = None
    radioactiveContainerClass: Optional[str] = None


@s(auto_attribs=True)
class DangerousGoodsDetailType:
    offeror: Optional[str] = None
    accessibility: Optional[str] = None
    emergencyContactNumber: Optional[str] = None
    options: List[str] = []
    containers: List[ContainerType] = JList[ContainerType]
    packaging: Optional[PackagingType] = JStruct[PackagingType]


@s(auto_attribs=True)
class CodCollectionAmountType:
    amount: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class PackageCODDetailType:
    codCollectionAmount: Optional[CodCollectionAmountType] = JStruct[CodCollectionAmountType]
    codCollectionType: Optional[str] = None


@s(auto_attribs=True)
class PackageSpecialServicesType:
    specialServiceTypes: List[str] = []
    signatureOptionType: List[str] = []
    alcoholDetail: Optional[AlcoholDetailType] = JStruct[AlcoholDetailType]
    dangerousGoodsDetail: Optional[DangerousGoodsDetailType] = JStruct[DangerousGoodsDetailType]
    packageCODDetail: Optional[PackageCODDetailType] = JStruct[PackageCODDetailType]
    pieceCountVerificationBoxCount: Optional[int] = None
    batteryDetails: List[BatteryDetailType] = JList[BatteryDetailType]
    dryIceWeight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class VariableHandlingChargeDetailType:
    rateType: Optional[str] = None
    percentValue: Optional[int] = None
    rateLevelType: Optional[str] = None
    fixedValue: Optional[FixedValueType] = JStruct[FixedValueType]
    rateElementBasis: Optional[str] = None


@s(auto_attribs=True)
class RequestedPackageLineItemType:
    subPackagingType: Optional[str] = None
    groupPackageCount: Optional[int] = None
    contentRecord: List[ContentRecordType] = JList[ContentRecordType]
    declaredValue: Optional[FixedValueType] = JStruct[FixedValueType]
    weight: Optional[WeightType] = JStruct[WeightType]
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    variableHandlingChargeDetail: Optional[VariableHandlingChargeDetailType] = JStruct[VariableHandlingChargeDetailType]
    packageSpecialServices: Optional[PackageSpecialServicesType] = JStruct[PackageSpecialServicesType]


@s(auto_attribs=True)
class ServiceTypeDetailType:
    carrierCode: Optional[str] = None
    description: Optional[str] = None
    serviceName: Optional[str] = None
    serviceCategory: Optional[str] = None


@s(auto_attribs=True)
class DeliveryOnInvoiceAcceptanceDetailType:
    recipient: Optional[BrokerClassType] = JStruct[BrokerClassType]


@s(auto_attribs=True)
class TionContactAndAddressType:
    address: Optional[ResponsiblePartyAddressType] = JStruct[ResponsiblePartyAddressType]
    contact: Optional[ResponsiblePartyContactType] = JStruct[ResponsiblePartyContactType]


@s(auto_attribs=True)
class HoldAtLocationDetailType:
    locationId: Optional[str] = None
    locationContactAndAddress: Optional[TionContactAndAddressType] = JStruct[TionContactAndAddressType]
    locationType: Optional[str] = None


@s(auto_attribs=True)
class HomeDeliveryPremiumDetailType:
    phoneNumber: Optional[NumberType] = JStruct[NumberType]
    shipTimestamp: Optional[str] = None
    homedeliveryPremiumType: Optional[str] = None


@s(auto_attribs=True)
class InternationalControlledExportDetailType:
    type: Optional[str] = None


@s(auto_attribs=True)
class InternationalTrafficInArmsRegulationsDetailType:
    licenseOrExemptionNumber: Optional[int] = None


@s(auto_attribs=True)
class DocumentReferenceType:
    documentType: Optional[str] = None
    customerReference: Optional[str] = None
    description: Optional[str] = None
    documentId: Optional[int] = None


@s(auto_attribs=True)
class LocaleType:
    country: Optional[str] = None
    language: Optional[str] = None


@s(auto_attribs=True)
class ProcessingOptionsType:
    options: List[str] = []


@s(auto_attribs=True)
class EmailLabelDetailRecipientType:
    emailAddress: Optional[str] = None
    optionsRequested: Optional[ProcessingOptionsType] = JStruct[ProcessingOptionsType]
    role: Optional[str] = None
    locale: Optional[LocaleType] = JStruct[LocaleType]


@s(auto_attribs=True)
class EmailLabelDetailType:
    recipients: List[EmailLabelDetailRecipientType] = JList[EmailLabelDetailRecipientType]
    message: Optional[str] = None


@s(auto_attribs=True)
class RecommendedDocumentSpecificationType:
    types: List[str] = []


@s(auto_attribs=True)
class ShipmentDryIceDetailType:
    totalWeight: Optional[WeightType] = JStruct[WeightType]
    packageCount: Optional[int] = None


@s(auto_attribs=True)
class PendingShipmentDetailType:
    pendingShipmentType: Optional[str] = None
    processingOptions: Optional[ProcessingOptionsType] = JStruct[ProcessingOptionsType]
    recommendedDocumentSpecification: Optional[RecommendedDocumentSpecificationType] = JStruct[RecommendedDocumentSpecificationType]
    emailLabelDetail: Optional[EmailLabelDetailType] = JStruct[EmailLabelDetailType]
    documentReferences: List[DocumentReferenceType] = JList[DocumentReferenceType]
    expirationTimeStamp: Optional[str] = None
    shipmentDryIceDetail: Optional[ShipmentDryIceDetailType] = JStruct[ShipmentDryIceDetailType]


@s(auto_attribs=True)
class ReturnShipmentDetailType:
    returnType: Optional[str] = None


@s(auto_attribs=True)
class AddTransportationChargesDetailType:
    rateType: Optional[str] = None
    rateLevelType: Optional[str] = None
    chargeLevelType: Optional[str] = None
    chargeType: Optional[str] = None


@s(auto_attribs=True)
class CodRecipientType:
    accountNumber: Optional[RecipientAccountNumberType] = JStruct[RecipientAccountNumberType]


@s(auto_attribs=True)
class ShipmentCODDetailType:
    addTransportationChargesDetail: Optional[AddTransportationChargesDetailType] = JStruct[AddTransportationChargesDetailType]
    codRecipient: Optional[CodRecipientType] = JStruct[CodRecipientType]
    remitToName: Optional[str] = None
    codCollectionType: Optional[str] = None
    financialInstitutionContactAndAddress: Optional[TionContactAndAddressType] = JStruct[TionContactAndAddressType]
    returnReferenceIndicatorType: Optional[str] = None


@s(auto_attribs=True)
class ShipmentSpecialServicesType:
    returnShipmentDetail: Optional[ReturnShipmentDetailType] = JStruct[ReturnShipmentDetailType]
    deliveryOnInvoiceAcceptanceDetail: Optional[DeliveryOnInvoiceAcceptanceDetailType] = JStruct[DeliveryOnInvoiceAcceptanceDetailType]
    internationalTrafficInArmsRegulationsDetail: Optional[InternationalTrafficInArmsRegulationsDetailType] = JStruct[InternationalTrafficInArmsRegulationsDetailType]
    pendingShipmentDetail: Optional[PendingShipmentDetailType] = JStruct[PendingShipmentDetailType]
    holdAtLocationDetail: Optional[HoldAtLocationDetailType] = JStruct[HoldAtLocationDetailType]
    shipmentCODDetail: Optional[ShipmentCODDetailType] = JStruct[ShipmentCODDetailType]
    shipmentDryIceDetail: Optional[ShipmentDryIceDetailType] = JStruct[ShipmentDryIceDetailType]
    internationalControlledExportDetail: Optional[InternationalControlledExportDetailType] = JStruct[InternationalControlledExportDetailType]
    homeDeliveryPremiumDetail: Optional[HomeDeliveryPremiumDetailType] = JStruct[HomeDeliveryPremiumDetailType]
    specialServiceTypes: List[str] = []


@s(auto_attribs=True)
class SmartPostInfoDetailType:
    ancillaryEndorsement: Optional[str] = None
    hubId: Optional[int] = None
    indicia: Optional[str] = None
    specialServices: Optional[str] = None


@s(auto_attribs=True)
class RequestedShipmentType:
    shipper: Optional[ShipperClassType] = JStruct[ShipperClassType]
    recipient: Optional[ShipperClassType] = JStruct[ShipperClassType]
    serviceType: Optional[str] = None
    emailNotificationDetail: Optional[EmailNotificationDetailType] = JStruct[EmailNotificationDetailType]
    preferredCurrency: Optional[str] = None
    rateRequestType: List[str] = []
    shipDateStamp: Optional[str] = None
    pickupType: Optional[str] = None
    requestedPackageLineItems: List[RequestedPackageLineItemType] = JList[RequestedPackageLineItemType]
    documentShipment: Optional[bool] = None
    variableHandlingChargeDetail: Optional[VariableHandlingChargeDetailType] = JStruct[VariableHandlingChargeDetailType]
    packagingType: Optional[str] = None
    totalPackageCount: Optional[int] = None
    totalWeight: Optional[float] = None
    shipmentSpecialServices: Optional[ShipmentSpecialServicesType] = JStruct[ShipmentSpecialServicesType]
    customsClearanceDetail: Optional[CustomsClearanceDetailType] = JStruct[CustomsClearanceDetailType]
    groupShipment: Optional[bool] = None
    serviceTypeDetail: Optional[ServiceTypeDetailType] = JStruct[ServiceTypeDetailType]
    smartPostInfoDetail: Optional[SmartPostInfoDetailType] = JStruct[SmartPostInfoDetailType]
    expressFreightDetail: Optional[ExpressFreightDetailType] = JStruct[ExpressFreightDetailType]
    groundShipment: Optional[bool] = None


@s(auto_attribs=True)
class RatingRequestType:
    accountNumber: Optional[RatingRequestAccountNumberType] = JStruct[RatingRequestAccountNumberType]
    rateRequestControlParameters: Optional[RateRequestControlParametersType] = JStruct[RateRequestControlParametersType]
    requestedShipment: Optional[RequestedShipmentType] = JStruct[RequestedShipmentType]
    carrierCodes: List[str] = []
