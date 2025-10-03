import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class RatingRequestAccountNumberType:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateRequestControlParametersType:
    returnTransitTimes: typing.Optional[bool] = None
    servicesNeededOnRateFailure: typing.Optional[bool] = None
    variableOptions: typing.Optional[str] = None
    rateSortOrder: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RecipientAccountNumberType:
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BrokerAddressType:
    streetLines: typing.Optional[typing.List[str]] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RecipientContactType:
    companyName: typing.Optional[str] = None
    faxNumber: typing.Optional[str] = None
    personName: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BrokerClassType:
    accountNumber: typing.Optional[RecipientAccountNumberType] = jstruct.JStruct[RecipientAccountNumberType]
    address: typing.Optional[BrokerAddressType] = jstruct.JStruct[BrokerAddressType]
    contact: typing.Optional[RecipientContactType] = jstruct.JStruct[RecipientContactType]


@attr.s(auto_attribs=True)
class BrokerAddressClassType:
    streetLines: typing.Optional[typing.List[str]] = None
    city: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    countryCode: typing.Optional[str] = None
    residential: typing.Optional[bool] = None
    classification: typing.Optional[str] = None
    geographicCoordinates: typing.Optional[str] = None
    urbanizationCode: typing.Optional[str] = None
    countryName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BrokerType:
    broker: typing.Optional[BrokerClassType] = jstruct.JStruct[BrokerClassType]
    type: typing.Optional[str] = None
    brokerCommitTimestamp: typing.Optional[str] = None
    brokerCommitDayOfWeek: typing.Optional[str] = None
    brokerLocationId: typing.Optional[str] = None
    brokerAddress: typing.Optional[BrokerAddressClassType] = jstruct.JStruct[BrokerAddressClassType]
    brokerToDestinationDays: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CommercialInvoiceType:
    shipmentPurpose: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FixedValueType:
    amount: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    units: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CommodityType:
    description: typing.Optional[str] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    quantity: typing.Optional[int] = None
    customsValue: typing.Optional[FixedValueType] = jstruct.JStruct[FixedValueType]
    unitPrice: typing.Optional[FixedValueType] = jstruct.JStruct[FixedValueType]
    numberOfPieces: typing.Optional[int] = None
    countryOfManufacture: typing.Optional[str] = None
    quantityUnits: typing.Optional[str] = None
    name: typing.Optional[str] = None
    harmonizedCode: typing.Optional[str] = None
    partNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponsiblePartyAddressType:
    streetLines: typing.Optional[typing.List[str]] = None
    city: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    countryCode: typing.Optional[str] = None
    residential: typing.Optional[bool] = None


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
    address: typing.Optional[ResponsiblePartyAddressType] = jstruct.JStruct[ResponsiblePartyAddressType]
    contact: typing.Optional[ResponsiblePartyContactType] = jstruct.JStruct[ResponsiblePartyContactType]
    accountNumber: typing.Optional[RatingRequestAccountNumberType] = jstruct.JStruct[RatingRequestAccountNumberType]


@attr.s(auto_attribs=True)
class PayorType:
    responsibleParty: typing.Optional[ResponsiblePartyType] = jstruct.JStruct[ResponsiblePartyType]


@attr.s(auto_attribs=True)
class DutiesPaymentType:
    payor: typing.Optional[PayorType] = jstruct.JStruct[PayorType]
    paymentType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomsClearanceDetailType:
    brokers: typing.Optional[typing.List[BrokerType]] = jstruct.JList[BrokerType]
    commercialInvoice: typing.Optional[CommercialInvoiceType] = jstruct.JStruct[CommercialInvoiceType]
    freightOnValue: typing.Optional[str] = None
    dutiesPayment: typing.Optional[DutiesPaymentType] = jstruct.JStruct[DutiesPaymentType]
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]


@attr.s(auto_attribs=True)
class PrintedReferenceType:
    printedReferenceType: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EmailNotificationDetailRecipientType:
    emailAddress: typing.Optional[str] = None
    notificationEventType: typing.Optional[typing.List[str]] = None
    smsDetail: typing.Any = None
    notificationFormatType: typing.Optional[str] = None
    emailNotificationRecipientType: typing.Optional[str] = None
    notificationType: typing.Optional[str] = None
    locale: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EmailNotificationDetailType:
    recipients: typing.Optional[typing.List[EmailNotificationDetailRecipientType]] = jstruct.JList[EmailNotificationDetailRecipientType]
    personalMessage: typing.Optional[str] = None
    PrintedReference: typing.Optional[PrintedReferenceType] = jstruct.JStruct[PrintedReferenceType]


@attr.s(auto_attribs=True)
class ExpressFreightDetailType:
    bookingConfirmationNumber: typing.Optional[str] = None
    shippersLoadAndCount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ShipperClassType:
    address: typing.Optional[ResponsiblePartyAddressType] = jstruct.JStruct[ResponsiblePartyAddressType]


@attr.s(auto_attribs=True)
class ContentRecordType:
    itemNumber: typing.Optional[str] = None
    receivedQuantity: typing.Optional[int] = None
    description: typing.Optional[str] = None
    partNumber: typing.Optional[str] = None


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
    material: typing.Optional[str] = None
    regulatorySubType: typing.Optional[str] = None
    packing: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NumberType:
    areaCode: typing.Optional[str] = None
    extension: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    personalIdentificationNumber: typing.Optional[str] = None
    localNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HazardousCommodityType:
    innerReceptacles: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class PackagingType:
    count: typing.Optional[int] = None
    units: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContainerType:
    offeror: typing.Optional[str] = None
    hazardousCommodities: typing.Optional[typing.List[HazardousCommodityType]] = jstruct.JList[HazardousCommodityType]
    numberOfContainers: typing.Optional[int] = None
    containerType: typing.Optional[str] = None
    emergencyContactNumber: typing.Optional[NumberType] = jstruct.JStruct[NumberType]
    packaging: typing.Optional[PackagingType] = jstruct.JStruct[PackagingType]
    packingType: typing.Optional[str] = None
    radioactiveContainerClass: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DangerousGoodsDetailType:
    offeror: typing.Optional[str] = None
    accessibility: typing.Optional[str] = None
    emergencyContactNumber: typing.Optional[str] = None
    options: typing.Optional[typing.List[str]] = None
    containers: typing.Optional[typing.List[ContainerType]] = jstruct.JList[ContainerType]
    packaging: typing.Optional[PackagingType] = jstruct.JStruct[PackagingType]


@attr.s(auto_attribs=True)
class CodCollectionAmountType:
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageCODDetailType:
    codCollectionAmount: typing.Optional[CodCollectionAmountType] = jstruct.JStruct[CodCollectionAmountType]
    codCollectionType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageSpecialServicesType:
    specialServiceTypes: typing.Optional[typing.List[str]] = None
    signatureOptionType: typing.Optional[typing.List[str]] = None
    alcoholDetail: typing.Optional[AlcoholDetailType] = jstruct.JStruct[AlcoholDetailType]
    dangerousGoodsDetail: typing.Optional[DangerousGoodsDetailType] = jstruct.JStruct[DangerousGoodsDetailType]
    packageCODDetail: typing.Optional[PackageCODDetailType] = jstruct.JStruct[PackageCODDetailType]
    pieceCountVerificationBoxCount: typing.Optional[int] = None
    batteryDetails: typing.Optional[typing.List[BatteryDetailType]] = jstruct.JList[BatteryDetailType]
    dryIceWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]


@attr.s(auto_attribs=True)
class VariableHandlingChargeDetailType:
    rateType: typing.Optional[str] = None
    percentValue: typing.Optional[int] = None
    rateLevelType: typing.Optional[str] = None
    fixedValue: typing.Optional[FixedValueType] = jstruct.JStruct[FixedValueType]
    rateElementBasis: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestedPackageLineItemType:
    subPackagingType: typing.Optional[str] = None
    groupPackageCount: typing.Optional[int] = None
    contentRecord: typing.Optional[typing.List[ContentRecordType]] = jstruct.JList[ContentRecordType]
    declaredValue: typing.Optional[FixedValueType] = jstruct.JStruct[FixedValueType]
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    variableHandlingChargeDetail: typing.Optional[VariableHandlingChargeDetailType] = jstruct.JStruct[VariableHandlingChargeDetailType]
    packageSpecialServices: typing.Optional[PackageSpecialServicesType] = jstruct.JStruct[PackageSpecialServicesType]


@attr.s(auto_attribs=True)
class ServiceTypeDetailType:
    carrierCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    serviceName: typing.Optional[str] = None
    serviceCategory: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryOnInvoiceAcceptanceDetailType:
    recipient: typing.Optional[BrokerClassType] = jstruct.JStruct[BrokerClassType]


@attr.s(auto_attribs=True)
class TionContactAndAddressType:
    address: typing.Optional[ResponsiblePartyAddressType] = jstruct.JStruct[ResponsiblePartyAddressType]
    contact: typing.Optional[ResponsiblePartyContactType] = jstruct.JStruct[ResponsiblePartyContactType]


@attr.s(auto_attribs=True)
class HoldAtLocationDetailType:
    locationId: typing.Optional[str] = None
    locationContactAndAddress: typing.Optional[TionContactAndAddressType] = jstruct.JStruct[TionContactAndAddressType]
    locationType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HomeDeliveryPremiumDetailType:
    phoneNumber: typing.Optional[NumberType] = jstruct.JStruct[NumberType]
    shipTimestamp: typing.Optional[str] = None
    homedeliveryPremiumType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalControlledExportDetailType:
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalTrafficInArmsRegulationsDetailType:
    licenseOrExemptionNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DocumentReferenceType:
    documentType: typing.Optional[str] = None
    customerReference: typing.Optional[str] = None
    description: typing.Optional[str] = None
    documentId: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class LocaleType:
    country: typing.Optional[str] = None
    language: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ProcessingOptionsType:
    options: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class EmailLabelDetailRecipientType:
    emailAddress: typing.Optional[str] = None
    optionsRequested: typing.Optional[ProcessingOptionsType] = jstruct.JStruct[ProcessingOptionsType]
    role: typing.Optional[str] = None
    locale: typing.Optional[LocaleType] = jstruct.JStruct[LocaleType]


@attr.s(auto_attribs=True)
class EmailLabelDetailType:
    recipients: typing.Optional[typing.List[EmailLabelDetailRecipientType]] = jstruct.JList[EmailLabelDetailRecipientType]
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RecommendedDocumentSpecificationType:
    types: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ShipmentDryIceDetailType:
    totalWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    packageCount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PendingShipmentDetailType:
    pendingShipmentType: typing.Optional[str] = None
    processingOptions: typing.Optional[ProcessingOptionsType] = jstruct.JStruct[ProcessingOptionsType]
    recommendedDocumentSpecification: typing.Optional[RecommendedDocumentSpecificationType] = jstruct.JStruct[RecommendedDocumentSpecificationType]
    emailLabelDetail: typing.Optional[EmailLabelDetailType] = jstruct.JStruct[EmailLabelDetailType]
    documentReferences: typing.Optional[typing.List[DocumentReferenceType]] = jstruct.JList[DocumentReferenceType]
    expirationTimeStamp: typing.Optional[str] = None
    shipmentDryIceDetail: typing.Optional[ShipmentDryIceDetailType] = jstruct.JStruct[ShipmentDryIceDetailType]


@attr.s(auto_attribs=True)
class ReturnShipmentDetailType:
    returnType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddTransportationChargesDetailType:
    rateType: typing.Optional[str] = None
    rateLevelType: typing.Optional[str] = None
    chargeLevelType: typing.Optional[str] = None
    chargeType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CodRecipientType:
    accountNumber: typing.Optional[RecipientAccountNumberType] = jstruct.JStruct[RecipientAccountNumberType]


@attr.s(auto_attribs=True)
class ShipmentCODDetailType:
    addTransportationChargesDetail: typing.Optional[AddTransportationChargesDetailType] = jstruct.JStruct[AddTransportationChargesDetailType]
    codRecipient: typing.Optional[CodRecipientType] = jstruct.JStruct[CodRecipientType]
    remitToName: typing.Optional[str] = None
    codCollectionType: typing.Optional[str] = None
    financialInstitutionContactAndAddress: typing.Optional[TionContactAndAddressType] = jstruct.JStruct[TionContactAndAddressType]
    returnReferenceIndicatorType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentSpecialServicesType:
    returnShipmentDetail: typing.Optional[ReturnShipmentDetailType] = jstruct.JStruct[ReturnShipmentDetailType]
    deliveryOnInvoiceAcceptanceDetail: typing.Optional[DeliveryOnInvoiceAcceptanceDetailType] = jstruct.JStruct[DeliveryOnInvoiceAcceptanceDetailType]
    internationalTrafficInArmsRegulationsDetail: typing.Optional[InternationalTrafficInArmsRegulationsDetailType] = jstruct.JStruct[InternationalTrafficInArmsRegulationsDetailType]
    pendingShipmentDetail: typing.Optional[PendingShipmentDetailType] = jstruct.JStruct[PendingShipmentDetailType]
    holdAtLocationDetail: typing.Optional[HoldAtLocationDetailType] = jstruct.JStruct[HoldAtLocationDetailType]
    shipmentCODDetail: typing.Optional[ShipmentCODDetailType] = jstruct.JStruct[ShipmentCODDetailType]
    shipmentDryIceDetail: typing.Optional[ShipmentDryIceDetailType] = jstruct.JStruct[ShipmentDryIceDetailType]
    internationalControlledExportDetail: typing.Optional[InternationalControlledExportDetailType] = jstruct.JStruct[InternationalControlledExportDetailType]
    homeDeliveryPremiumDetail: typing.Optional[HomeDeliveryPremiumDetailType] = jstruct.JStruct[HomeDeliveryPremiumDetailType]
    specialServiceTypes: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class SmartPostInfoDetailType:
    ancillaryEndorsement: typing.Optional[str] = None
    hubId: typing.Optional[int] = None
    indicia: typing.Optional[str] = None
    specialServices: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestedShipmentType:
    shipper: typing.Optional[ShipperClassType] = jstruct.JStruct[ShipperClassType]
    recipient: typing.Optional[ShipperClassType] = jstruct.JStruct[ShipperClassType]
    serviceType: typing.Optional[str] = None
    emailNotificationDetail: typing.Optional[EmailNotificationDetailType] = jstruct.JStruct[EmailNotificationDetailType]
    preferredCurrency: typing.Optional[str] = None
    rateRequestType: typing.Optional[typing.List[str]] = None
    shipDateStamp: typing.Optional[str] = None
    pickupType: typing.Optional[str] = None
    requestedPackageLineItems: typing.Optional[typing.List[RequestedPackageLineItemType]] = jstruct.JList[RequestedPackageLineItemType]
    documentShipment: typing.Optional[bool] = None
    variableHandlingChargeDetail: typing.Optional[VariableHandlingChargeDetailType] = jstruct.JStruct[VariableHandlingChargeDetailType]
    packagingType: typing.Optional[str] = None
    totalPackageCount: typing.Optional[int] = None
    totalWeight: typing.Optional[float] = None
    shipmentSpecialServices: typing.Optional[ShipmentSpecialServicesType] = jstruct.JStruct[ShipmentSpecialServicesType]
    customsClearanceDetail: typing.Optional[CustomsClearanceDetailType] = jstruct.JStruct[CustomsClearanceDetailType]
    groupShipment: typing.Optional[bool] = None
    serviceTypeDetail: typing.Optional[ServiceTypeDetailType] = jstruct.JStruct[ServiceTypeDetailType]
    smartPostInfoDetail: typing.Optional[SmartPostInfoDetailType] = jstruct.JStruct[SmartPostInfoDetailType]
    expressFreightDetail: typing.Optional[ExpressFreightDetailType] = jstruct.JStruct[ExpressFreightDetailType]
    groundShipment: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class RatingRequestType:
    accountNumber: typing.Optional[RatingRequestAccountNumberType] = jstruct.JStruct[RatingRequestAccountNumberType]
    rateRequestControlParameters: typing.Optional[RateRequestControlParametersType] = jstruct.JStruct[RateRequestControlParametersType]
    requestedShipment: typing.Optional[RequestedShipmentType] = jstruct.JStruct[RequestedShipmentType]
    carrierCodes: typing.Optional[typing.List[str]] = None
