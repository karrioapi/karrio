from attr import s
from typing import Optional, Any, List, Union
from jstruct import JList, JStruct


@s(auto_attribs=True)
class AlertType:
    code: Optional[str] = None
    alertType: Optional[str] = None
    message: Optional[str] = None
    parameterList: List[Any] = []


@s(auto_attribs=True)
class AccessorDetailType:
    password: Optional[str] = None
    role: Optional[str] = None
    emailLabelUrl: Optional[str] = None
    userId: Optional[str] = None


@s(auto_attribs=True)
class AccessDetailType:
    accessorDetails: List[AccessorDetailType] = JList[AccessorDetailType]


@s(auto_attribs=True)
class UploadDocumentReferenceDetailType:
    documentType: Optional[str] = None
    documentReference: Optional[str] = None
    description: Optional[str] = None
    documentId: Optional[str] = None


@s(auto_attribs=True)
class CompletedEtdDetailType:
    folderId: Optional[str] = None
    type: Optional[str] = None
    uploadDocumentReferenceDetails: List[UploadDocumentReferenceDetailType] = JList[UploadDocumentReferenceDetailType]


@s(auto_attribs=True)
class AddressType:
    streetLines: List[str] = []
    city: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    postalCode: Optional[int] = None
    countryCode: Optional[str] = None
    residential: Optional[bool] = None


@s(auto_attribs=True)
class ContactType:
    personName: Optional[str] = None
    tollFreePhoneNumber: Optional[int] = None
    emailAddress: Optional[str] = None
    phoneNumber: Optional[int] = None
    phoneExtension: Optional[int] = None
    faxNumber: Optional[int] = None
    pagerNumber: Optional[int] = None
    companyName: Optional[str] = None
    title: Optional[str] = None


@s(auto_attribs=True)
class HoldingLocationType:
    address: Optional[AddressType] = JStruct[AddressType]
    contact: Optional[ContactType] = JStruct[ContactType]


@s(auto_attribs=True)
class CompletedHoldAtLocationDetailType:
    holdingLocationType: Optional[str] = None
    holdingLocation: Optional[HoldingLocationType] = JStruct[HoldingLocationType]


@s(auto_attribs=True)
class WeightType:
    units: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class HazardousCommodityDescriptionType:
    sequenceNumber: Optional[int] = None
    packingInstructions: Optional[str] = None
    subsidiaryClasses: List[str] = []
    labelText: Optional[str] = None
    tunnelRestrictionCode: Optional[str] = None
    specialProvisions: Optional[str] = None
    properShippingNameAndDescription: Optional[str] = None
    technicalName: Optional[str] = None
    symbols: Optional[str] = None
    authorization: Optional[str] = None
    attributes: List[str] = []
    id: Optional[int] = None
    packingGroup: Optional[str] = None
    properShippingName: Optional[str] = None
    hazardClass: Optional[str] = None


@s(auto_attribs=True)
class NetExplosiveDetailType:
    amount: Optional[int] = None
    units: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class PackingDetailsType:
    packingInstructions: Optional[str] = None
    cargoAircraftOnly: Optional[bool] = None


@s(auto_attribs=True)
class OptionsDescriptionType:
    sequenceNumber: Optional[int] = None
    processingOptions: List[str] = []
    subsidiaryClasses: List[str] = []
    labelText: Optional[str] = None
    technicalName: Optional[str] = None
    packingDetails: Optional[PackingDetailsType] = JStruct[PackingDetailsType]
    authorization: Optional[str] = None
    reportableQuantity: Optional[bool] = None
    percentage: Optional[float] = None
    id: Optional[int] = None
    packingGroup: Optional[str] = None
    properShippingName: Optional[str] = None
    hazardClass: Optional[str] = None


@s(auto_attribs=True)
class QuantityType:
    quantityType: Optional[str] = None
    amount: Optional[float] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class InnerReceptacleType:
    quantity: Optional[QuantityType] = JStruct[QuantityType]


@s(auto_attribs=True)
class OptionsOptionsType:
    labelTextOption: Optional[str] = None
    customerSuppliedLabelText: Optional[str] = None


@s(auto_attribs=True)
class HazardousCommodityOptionsType:
    quantity: Optional[QuantityType] = JStruct[QuantityType]
    innerReceptacles: List[InnerReceptacleType] = JList[InnerReceptacleType]
    options: Optional[OptionsOptionsType] = JStruct[OptionsOptionsType]
    description: Optional[OptionsDescriptionType] = JStruct[OptionsDescriptionType]


@s(auto_attribs=True)
class HazardousCommodityType:
    quantity: Optional[QuantityType] = JStruct[QuantityType]
    options: Optional[HazardousCommodityOptionsType] = JStruct[HazardousCommodityOptionsType]
    description: Optional[HazardousCommodityDescriptionType] = JStruct[HazardousCommodityDescriptionType]
    netExplosiveDetail: Optional[NetExplosiveDetailType] = JStruct[NetExplosiveDetailType]
    massPoints: Optional[int] = None


@s(auto_attribs=True)
class ContainerType:
    qvalue: Optional[int] = None
    hazardousCommodities: List[HazardousCommodityType] = JList[HazardousCommodityType]


@s(auto_attribs=True)
class HazardousPackageDetailType:
    regulation: Optional[str] = None
    accessibility: Optional[str] = None
    labelType: Optional[str] = None
    containers: List[ContainerType] = JList[ContainerType]
    cargoAircraftOnly: Optional[bool] = None
    referenceId: Optional[int] = None
    radioactiveTransportIndex: Optional[float] = None


@s(auto_attribs=True)
class BarcodeType:
    type: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class BarcodesType:
    binaryBarcodes: List[BarcodeType] = JList[BarcodeType]
    stringBarcodes: List[BarcodeType] = JList[BarcodeType]


@s(auto_attribs=True)
class OperationalInstructionType:
    number: Optional[int] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class CompletedPackageDetailOperationalDetailType:
    astraHandlingText: Optional[str] = None
    barcodes: Optional[BarcodesType] = JStruct[BarcodesType]
    operationalInstructions: List[OperationalInstructionType] = JList[OperationalInstructionType]


@s(auto_attribs=True)
class PackageRateDetailSurchargeType:
    amount: Optional[str] = None
    surchargeType: Optional[str] = None
    level: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class PackageRateDetailType:
    ratedWeightMethod: Optional[str] = None
    totalFreightDiscounts: Optional[float] = None
    totalTaxes: Optional[float] = None
    minimumChargeType: Optional[str] = None
    baseCharge: Optional[float] = None
    totalRebates: Optional[float] = None
    rateType: Optional[str] = None
    billingWeight: Optional[WeightType] = JStruct[WeightType]
    netFreight: Optional[float] = None
    surcharges: List[PackageRateDetailSurchargeType] = JList[PackageRateDetailSurchargeType]
    totalSurcharges: Optional[float] = None
    netFedExCharge: Optional[float] = None
    netCharge: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class PackageRatingType:
    effectiveNetDiscount: Optional[int] = None
    actualRateType: Optional[str] = None
    packageRateDetails: List[PackageRateDetailType] = JList[PackageRateDetailType]


@s(auto_attribs=True)
class TrackingIDType:
    formId: Optional[str] = None
    trackingIdType: Optional[str] = None
    uspsApplicationId: Optional[int] = None
    trackingNumber: Optional[str] = None


@s(auto_attribs=True)
class CompletedPackageDetailType:
    sequenceNumber: Optional[int] = None
    operationalDetail: Optional[CompletedPackageDetailOperationalDetailType] = JStruct[CompletedPackageDetailOperationalDetailType]
    signatureOption: Optional[str] = None
    trackingIds: List[TrackingIDType] = JList[TrackingIDType]
    groupNumber: Optional[int] = None
    oversizeClass: Optional[str] = None
    packageRating: Optional[PackageRatingType] = JStruct[PackageRatingType]
    dryIceWeight: Optional[WeightType] = JStruct[WeightType]
    hazardousPackageDetail: Optional[HazardousPackageDetailType] = JStruct[HazardousPackageDetailType]


@s(auto_attribs=True)
class GenerationDetailType:
    type: Optional[str] = None
    minimumCopiesRequired: Optional[int] = None
    letterhead: Optional[str] = None
    electronicSignature: Optional[str] = None


@s(auto_attribs=True)
class DocumentRequirementsType:
    requiredDocuments: List[str] = []
    prohibitedDocuments: List[str] = []
    generationDetails: List[GenerationDetailType] = JList[GenerationDetailType]


@s(auto_attribs=True)
class LicenseOrPermitDetailType:
    number: Optional[int] = None
    effectiveDate: Optional[str] = None
    expirationDate: Optional[str] = None


@s(auto_attribs=True)
class AdrLicenseType:
    licenseOrPermitDetail: Optional[LicenseOrPermitDetailType] = JStruct[LicenseOrPermitDetailType]


@s(auto_attribs=True)
class ProcessingOptionsType:
    options: List[str] = []


@s(auto_attribs=True)
class DryIceDetailType:
    totalWeight: Optional[WeightType] = JStruct[WeightType]
    packageCount: Optional[int] = None
    processingOptions: Optional[ProcessingOptionsType] = JStruct[ProcessingOptionsType]


@s(auto_attribs=True)
class HazardousSummaryDetailType:
    smallQuantityExceptionPackageCount: Optional[int] = None


@s(auto_attribs=True)
class HazardousShipmentDetailType:
    hazardousSummaryDetail: Optional[HazardousSummaryDetailType] = JStruct[HazardousSummaryDetailType]
    adrLicense: Optional[AdrLicenseType] = JStruct[AdrLicenseType]
    dryIceDetail: Optional[DryIceDetailType] = JStruct[DryIceDetailType]


@s(auto_attribs=True)
class CompletedShipmentDetailOperationalDetailType:
    originServiceArea: Optional[str] = None
    serviceCode: Optional[str] = None
    airportId: Optional[str] = None
    postalCode: Optional[int] = None
    scac: Optional[str] = None
    deliveryDay: Optional[str] = None
    originLocationId: Optional[str] = None
    countryCode: Optional[str] = None
    astraDescription: Optional[str] = None
    originLocationNumber: Optional[int] = None
    deliveryDate: Optional[str] = None
    deliveryEligibilities: List[str] = []
    ineligibleForMoneyBackGuarantee: Optional[bool] = None
    maximumTransitTime: Optional[str] = None
    destinationLocationStateOrProvinceCode: Optional[str] = None
    astraPlannedServiceLevel: Optional[str] = None
    destinationLocationId: Optional[str] = None
    transitTime: Optional[str] = None
    stateOrProvinceCode: Optional[str] = None
    destinationLocationNumber: Optional[int] = None
    packagingCode: Optional[str] = None
    commitDate: Optional[str] = None
    publishedDeliveryTime: Optional[str] = None
    ursaSuffixCode: Optional[str] = None
    ursaPrefixCode: Optional[str] = None
    destinationServiceArea: Optional[str] = None
    commitDay: Optional[str] = None
    customTransitTime: Optional[str] = None


@s(auto_attribs=True)
class NameType:
    type: Optional[str] = None
    encoding: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class ServiceDescriptionType:
    serviceType: Optional[str] = None
    code: Optional[str] = None
    names: List[NameType] = JList[NameType]
    operatingOrgCodes: List[str] = []
    astraDescription: Optional[str] = None
    description: Optional[str] = None
    serviceId: Optional[str] = None
    serviceCategory: Optional[str] = None


@s(auto_attribs=True)
class PartType:
    documentPartSequenceNumber: Optional[int] = None
    image: Optional[str] = None


@s(auto_attribs=True)
class ShipmentDocumentType:
    type: Optional[str] = None
    shippingDocumentDisposition: Optional[str] = None
    imageType: Optional[str] = None
    resolution: Optional[int] = None
    copiesToPrint: Optional[int] = None
    parts: List[PartType] = JList[PartType]


@s(auto_attribs=True)
class CurrencyExchangeRateType:
    rate: Optional[float] = None
    fromCurrency: Optional[str] = None
    intoCurrency: Optional[str] = None


@s(auto_attribs=True)
class FreightDiscountType:
    amount: Optional[float] = None
    rateDiscountType: Optional[str] = None
    percent: Optional[float] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class ShipmentRateDetailSurchargeType:
    amount: Union[float, Any, str]
    surchargeType: Optional[str] = None
    level: Optional[str] = None
    description: Optional[str] = None


@s(auto_attribs=True)
class TaxType:
    amount: Optional[float] = None
    level: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None


@s(auto_attribs=True)
class ShipmentRateDetailType:
    rateZone: Optional[str] = None
    ratedWeightMethod: Optional[str] = None
    totalDutiesTaxesAndFees: Optional[float] = None
    pricingCode: Optional[str] = None
    totalFreightDiscounts: Optional[float] = None
    totalTaxes: Optional[float] = None
    totalDutiesAndTaxes: Optional[float] = None
    totalAncillaryFeesAndTaxes: Optional[float] = None
    taxes: List[TaxType] = JList[TaxType]
    totalRebates: Optional[float] = None
    fuelSurchargePercent: Optional[float] = None
    currencyExchangeRate: Optional[CurrencyExchangeRateType] = JStruct[CurrencyExchangeRateType]
    totalNetFreight: Optional[float] = None
    totalNetFedExCharge: Optional[float] = None
    shipmentLegRateDetails: List[Any] = []
    dimDivisor: Optional[int] = None
    rateType: Optional[str] = None
    surcharges: List[ShipmentRateDetailSurchargeType] = JList[ShipmentRateDetailSurchargeType]
    totalSurcharges: Optional[float] = None
    totalBillingWeight: Optional[WeightType] = JStruct[WeightType]
    freightDiscounts: List[FreightDiscountType] = JList[FreightDiscountType]
    rateScale: Optional[str] = None
    totalNetCharge: Optional[float] = None
    totalBaseCharge: Optional[float] = None
    totalNetChargeWithDutiesAndTaxes: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class ShipmentRatingType:
    actualRateType: Optional[str] = None
    shipmentRateDetails: List[ShipmentRateDetailType] = JList[ShipmentRateDetailType]


@s(auto_attribs=True)
class CompletedShipmentDetailType:
    completedPackageDetails: List[CompletedPackageDetailType] = JList[CompletedPackageDetailType]
    operationalDetail: Optional[CompletedShipmentDetailOperationalDetailType] = JStruct[CompletedShipmentDetailOperationalDetailType]
    carrierCode: Optional[str] = None
    completedHoldAtLocationDetail: Optional[CompletedHoldAtLocationDetailType] = JStruct[CompletedHoldAtLocationDetailType]
    completedEtdDetail: Optional[CompletedEtdDetailType] = JStruct[CompletedEtdDetailType]
    packagingDescription: Optional[str] = None
    masterTrackingId: Optional[TrackingIDType] = JStruct[TrackingIDType]
    serviceDescription: Optional[ServiceDescriptionType] = JStruct[ServiceDescriptionType]
    usDomestic: Optional[bool] = None
    hazardousShipmentDetail: Optional[HazardousShipmentDetailType] = JStruct[HazardousShipmentDetailType]
    shipmentRating: Optional[ShipmentRatingType] = JStruct[ShipmentRatingType]
    documentRequirements: Optional[DocumentRequirementsType] = JStruct[DocumentRequirementsType]
    exportComplianceStatement: Optional[str] = None
    accessDetail: Optional[AccessDetailType] = JStruct[AccessDetailType]
    shipmentDocuments: List[ShipmentDocumentType] = JList[ShipmentDocumentType]


@s(auto_attribs=True)
class CustomerReferenceType:
    customerReferenceType: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class DocumentType:
    contentKey: Optional[str] = None
    copiesToPrint: Optional[int] = None
    contentType: Optional[str] = None
    trackingNumber: Optional[str] = None
    docType: Optional[str] = None
    alerts: List[AlertType] = JList[AlertType]
    encodedLabel: Optional[str] = None
    url: Optional[str] = None


@s(auto_attribs=True)
class TransactionDetailType:
    transactionDetails: Optional[str] = None
    transactionId: Optional[int] = None


@s(auto_attribs=True)
class PieceResponseType:
    netChargeAmount: Optional[float] = None
    transactionDetails: List[TransactionDetailType] = JList[TransactionDetailType]
    packageDocuments: List[DocumentType] = JList[DocumentType]
    acceptanceTrackingNumber: Optional[str] = None
    serviceCategory: Optional[str] = None
    listCustomerTotalCharge: Optional[str] = None
    deliveryTimestamp: Optional[str] = None
    trackingIdType: Optional[str] = None
    additionalChargesDiscount: Optional[float] = None
    netListRateAmount: Optional[float] = None
    baseRateAmount: Optional[float] = None
    packageSequenceNumber: Optional[int] = None
    netDiscountAmount: Optional[float] = None
    codcollectionAmount: Optional[float] = None
    masterTrackingNumber: Optional[str] = None
    acceptanceType: Optional[str] = None
    trackingNumber: Optional[str] = None
    successful: Optional[bool] = None
    customerReferences: List[CustomerReferenceType] = JList[CustomerReferenceType]
    netRateAmount: Optional[float] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class ParameterType:
    id: Optional[str] = None
    value: Optional[str] = None


@s(auto_attribs=True)
class AdvisoryType:
    code: Optional[str] = None
    text: Optional[str] = None
    parameters: List[ParameterType] = JList[ParameterType]
    localizedText: Optional[str] = None


@s(auto_attribs=True)
class WaiverType:
    advisories: List[AdvisoryType] = JList[AdvisoryType]
    description: Optional[str] = None
    id: Optional[str] = None


@s(auto_attribs=True)
class ProhibitionType:
    derivedHarmonizedCode: Optional[str] = None
    advisory: Optional[AdvisoryType] = JStruct[AdvisoryType]
    commodityIndex: Optional[int] = None
    source: Optional[str] = None
    categories: List[str] = []
    type: Optional[str] = None
    waiver: Optional[WaiverType] = JStruct[WaiverType]
    status: Optional[str] = None


@s(auto_attribs=True)
class RegulatoryAdvisoryType:
    prohibitions: List[ProhibitionType] = JList[ProhibitionType]


@s(auto_attribs=True)
class ShipmentAdvisoryDetailsType:
    regulatoryAdvisory: Optional[RegulatoryAdvisoryType] = JStruct[RegulatoryAdvisoryType]


@s(auto_attribs=True)
class TransactionShipmentType:
    serviceType: Optional[str] = None
    shipDatestamp: Optional[str] = None
    serviceCategory: Optional[str] = None
    shipmentDocuments: List[DocumentType] = JList[DocumentType]
    pieceResponses: List[PieceResponseType] = JList[PieceResponseType]
    serviceName: Optional[str] = None
    alerts: List[AlertType] = JList[AlertType]
    completedShipmentDetail: Optional[CompletedShipmentDetailType] = JStruct[CompletedShipmentDetailType]
    shipmentAdvisoryDetails: Optional[ShipmentAdvisoryDetailsType] = JStruct[ShipmentAdvisoryDetailsType]
    masterTrackingNumber: Optional[str] = None


@s(auto_attribs=True)
class OutputType:
    transactionShipments: List[TransactionShipmentType] = JList[TransactionShipmentType]
    alerts: List[AlertType] = JList[AlertType]
    jobId: Optional[str] = None


@s(auto_attribs=True)
class ShippingResponseType:
    transactionId: Optional[str] = None
    customerTransactionId: Optional[str] = None
    output: Optional[OutputType] = JStruct[OutputType]
