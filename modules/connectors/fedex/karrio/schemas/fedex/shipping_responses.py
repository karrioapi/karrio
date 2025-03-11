import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AlertType:
    code: typing.Optional[str] = None
    alertType: typing.Optional[str] = None
    message: typing.Optional[str] = None
    parameterList: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class AccessorDetailType:
    password: typing.Optional[str] = None
    role: typing.Optional[str] = None
    emailLabelUrl: typing.Optional[str] = None
    userId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AccessDetailType:
    accessorDetails: typing.Optional[typing.List[AccessorDetailType]] = jstruct.JList[AccessorDetailType]


@attr.s(auto_attribs=True)
class UploadDocumentReferenceDetailType:
    documentType: typing.Optional[str] = None
    documentReference: typing.Optional[str] = None
    description: typing.Optional[str] = None
    documentId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CompletedEtdDetailType:
    folderId: typing.Optional[str] = None
    type: typing.Optional[str] = None
    uploadDocumentReferenceDetails: typing.Optional[typing.List[UploadDocumentReferenceDetailType]] = jstruct.JList[UploadDocumentReferenceDetailType]


@attr.s(auto_attribs=True)
class AddressType:
    streetLines: typing.Optional[typing.List[str]] = None
    city: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    countryCode: typing.Optional[str] = None
    residential: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ContactType:
    personName: typing.Optional[str] = None
    tollFreePhoneNumber: typing.Optional[int] = None
    emailAddress: typing.Optional[str] = None
    phoneNumber: typing.Optional[int] = None
    phoneExtension: typing.Optional[int] = None
    faxNumber: typing.Optional[int] = None
    pagerNumber: typing.Optional[int] = None
    companyName: typing.Optional[str] = None
    title: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HoldingLocationType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]


@attr.s(auto_attribs=True)
class CompletedHoldAtLocationDetailType:
    holdingLocationType: typing.Optional[str] = None
    holdingLocation: typing.Optional[HoldingLocationType] = jstruct.JStruct[HoldingLocationType]


@attr.s(auto_attribs=True)
class WeightType:
    units: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class HazardousCommodityDescriptionType:
    sequenceNumber: typing.Optional[int] = None
    packingInstructions: typing.Optional[str] = None
    subsidiaryClasses: typing.Optional[typing.List[str]] = None
    labelText: typing.Optional[str] = None
    tunnelRestrictionCode: typing.Optional[str] = None
    specialProvisions: typing.Optional[str] = None
    properShippingNameAndDescription: typing.Optional[str] = None
    technicalName: typing.Optional[str] = None
    symbols: typing.Optional[str] = None
    authorization: typing.Optional[str] = None
    attributes: typing.Optional[typing.List[str]] = None
    id: typing.Optional[int] = None
    packingGroup: typing.Optional[str] = None
    properShippingName: typing.Optional[str] = None
    hazardClass: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NetExplosiveDetailType:
    amount: typing.Optional[int] = None
    units: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackingDetailsType:
    packingInstructions: typing.Optional[str] = None
    cargoAircraftOnly: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class OptionsDescriptionType:
    sequenceNumber: typing.Optional[int] = None
    processingOptions: typing.Optional[typing.List[str]] = None
    subsidiaryClasses: typing.Optional[typing.List[str]] = None
    labelText: typing.Optional[str] = None
    technicalName: typing.Optional[str] = None
    packingDetails: typing.Optional[PackingDetailsType] = jstruct.JStruct[PackingDetailsType]
    authorization: typing.Optional[str] = None
    reportableQuantity: typing.Optional[bool] = None
    percentage: typing.Optional[float] = None
    id: typing.Optional[int] = None
    packingGroup: typing.Optional[str] = None
    properShippingName: typing.Optional[str] = None
    hazardClass: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class QuantityType:
    quantityType: typing.Optional[str] = None
    amount: typing.Optional[float] = None
    units: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InnerReceptacleType:
    quantity: typing.Optional[QuantityType] = jstruct.JStruct[QuantityType]


@attr.s(auto_attribs=True)
class OptionsOptionsType:
    labelTextOption: typing.Optional[str] = None
    customerSuppliedLabelText: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HazardousCommodityOptionsType:
    quantity: typing.Optional[QuantityType] = jstruct.JStruct[QuantityType]
    innerReceptacles: typing.Optional[typing.List[InnerReceptacleType]] = jstruct.JList[InnerReceptacleType]
    options: typing.Optional[OptionsOptionsType] = jstruct.JStruct[OptionsOptionsType]
    description: typing.Optional[OptionsDescriptionType] = jstruct.JStruct[OptionsDescriptionType]


@attr.s(auto_attribs=True)
class HazardousCommodityType:
    quantity: typing.Optional[QuantityType] = jstruct.JStruct[QuantityType]
    options: typing.Optional[HazardousCommodityOptionsType] = jstruct.JStruct[HazardousCommodityOptionsType]
    description: typing.Optional[HazardousCommodityDescriptionType] = jstruct.JStruct[HazardousCommodityDescriptionType]
    netExplosiveDetail: typing.Optional[NetExplosiveDetailType] = jstruct.JStruct[NetExplosiveDetailType]
    massPoints: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ContainerType:
    qvalue: typing.Optional[int] = None
    hazardousCommodities: typing.Optional[typing.List[HazardousCommodityType]] = jstruct.JList[HazardousCommodityType]


@attr.s(auto_attribs=True)
class HazardousPackageDetailType:
    regulation: typing.Optional[str] = None
    accessibility: typing.Optional[str] = None
    labelType: typing.Optional[str] = None
    containers: typing.Optional[typing.List[ContainerType]] = jstruct.JList[ContainerType]
    cargoAircraftOnly: typing.Optional[bool] = None
    referenceId: typing.Optional[int] = None
    radioactiveTransportIndex: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class BarcodeType:
    type: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BarcodesType:
    binaryBarcodes: typing.Optional[typing.List[BarcodeType]] = jstruct.JList[BarcodeType]
    stringBarcodes: typing.Optional[typing.List[BarcodeType]] = jstruct.JList[BarcodeType]


@attr.s(auto_attribs=True)
class OperationalInstructionType:
    number: typing.Optional[int] = None
    content: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CompletedPackageDetailOperationalDetailType:
    astraHandlingText: typing.Optional[str] = None
    barcodes: typing.Optional[BarcodesType] = jstruct.JStruct[BarcodesType]
    operationalInstructions: typing.Optional[typing.List[OperationalInstructionType]] = jstruct.JList[OperationalInstructionType]


@attr.s(auto_attribs=True)
class PackageRateDetailSurchargeType:
    amount: typing.Optional[str] = None
    surchargeType: typing.Optional[str] = None
    level: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageRateDetailType:
    ratedWeightMethod: typing.Optional[str] = None
    totalFreightDiscounts: typing.Optional[float] = None
    totalTaxes: typing.Optional[float] = None
    minimumChargeType: typing.Optional[str] = None
    baseCharge: typing.Optional[float] = None
    totalRebates: typing.Optional[float] = None
    rateType: typing.Optional[str] = None
    billingWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    netFreight: typing.Optional[float] = None
    surcharges: typing.Optional[typing.List[PackageRateDetailSurchargeType]] = jstruct.JList[PackageRateDetailSurchargeType]
    totalSurcharges: typing.Optional[float] = None
    netFedExCharge: typing.Optional[float] = None
    netCharge: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageRatingType:
    effectiveNetDiscount: typing.Optional[int] = None
    actualRateType: typing.Optional[str] = None
    packageRateDetails: typing.Optional[typing.List[PackageRateDetailType]] = jstruct.JList[PackageRateDetailType]


@attr.s(auto_attribs=True)
class TrackingIDType:
    formId: typing.Optional[str] = None
    trackingIdType: typing.Optional[str] = None
    uspsApplicationId: typing.Optional[int] = None
    trackingNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CompletedPackageDetailType:
    sequenceNumber: typing.Optional[int] = None
    operationalDetail: typing.Optional[CompletedPackageDetailOperationalDetailType] = jstruct.JStruct[CompletedPackageDetailOperationalDetailType]
    signatureOption: typing.Optional[str] = None
    trackingIds: typing.Optional[typing.List[TrackingIDType]] = jstruct.JList[TrackingIDType]
    groupNumber: typing.Optional[int] = None
    oversizeClass: typing.Optional[str] = None
    packageRating: typing.Optional[PackageRatingType] = jstruct.JStruct[PackageRatingType]
    dryIceWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    hazardousPackageDetail: typing.Optional[HazardousPackageDetailType] = jstruct.JStruct[HazardousPackageDetailType]


@attr.s(auto_attribs=True)
class GenerationDetailType:
    type: typing.Optional[str] = None
    minimumCopiesRequired: typing.Optional[int] = None
    letterhead: typing.Optional[str] = None
    electronicSignature: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DocumentRequirementsType:
    requiredDocuments: typing.Optional[typing.List[str]] = None
    prohibitedDocuments: typing.Optional[typing.List[str]] = None
    generationDetails: typing.Optional[typing.List[GenerationDetailType]] = jstruct.JList[GenerationDetailType]


@attr.s(auto_attribs=True)
class LicenseOrPermitDetailType:
    number: typing.Optional[int] = None
    effectiveDate: typing.Optional[str] = None
    expirationDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdrLicenseType:
    licenseOrPermitDetail: typing.Optional[LicenseOrPermitDetailType] = jstruct.JStruct[LicenseOrPermitDetailType]


@attr.s(auto_attribs=True)
class ProcessingOptionsType:
    options: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class DryIceDetailType:
    totalWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    packageCount: typing.Optional[int] = None
    processingOptions: typing.Optional[ProcessingOptionsType] = jstruct.JStruct[ProcessingOptionsType]


@attr.s(auto_attribs=True)
class HazardousSummaryDetailType:
    smallQuantityExceptionPackageCount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class HazardousShipmentDetailType:
    hazardousSummaryDetail: typing.Optional[HazardousSummaryDetailType] = jstruct.JStruct[HazardousSummaryDetailType]
    adrLicense: typing.Optional[AdrLicenseType] = jstruct.JStruct[AdrLicenseType]
    dryIceDetail: typing.Optional[DryIceDetailType] = jstruct.JStruct[DryIceDetailType]


@attr.s(auto_attribs=True)
class CompletedShipmentDetailOperationalDetailType:
    originServiceArea: typing.Optional[str] = None
    serviceCode: typing.Optional[str] = None
    airportId: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    scac: typing.Optional[str] = None
    deliveryDay: typing.Optional[str] = None
    originLocationId: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    astraDescription: typing.Optional[str] = None
    originLocationNumber: typing.Optional[int] = None
    deliveryDate: typing.Optional[str] = None
    deliveryEligibilities: typing.Optional[typing.List[str]] = None
    ineligibleForMoneyBackGuarantee: typing.Optional[bool] = None
    maximumTransitTime: typing.Optional[str] = None
    destinationLocationStateOrProvinceCode: typing.Optional[str] = None
    astraPlannedServiceLevel: typing.Optional[str] = None
    destinationLocationId: typing.Optional[str] = None
    transitTime: typing.Optional[str] = None
    stateOrProvinceCode: typing.Optional[str] = None
    destinationLocationNumber: typing.Optional[int] = None
    packagingCode: typing.Optional[str] = None
    commitDate: typing.Optional[str] = None
    publishedDeliveryTime: typing.Optional[str] = None
    ursaSuffixCode: typing.Optional[str] = None
    ursaPrefixCode: typing.Optional[str] = None
    destinationServiceArea: typing.Optional[str] = None
    commitDay: typing.Optional[str] = None
    customTransitTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NameType:
    type: typing.Optional[str] = None
    encoding: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceDescriptionType:
    serviceType: typing.Optional[str] = None
    code: typing.Optional[str] = None
    names: typing.Optional[typing.List[NameType]] = jstruct.JList[NameType]
    operatingOrgCodes: typing.Optional[typing.List[str]] = None
    astraDescription: typing.Optional[str] = None
    description: typing.Optional[str] = None
    serviceId: typing.Optional[str] = None
    serviceCategory: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PartType:
    documentPartSequenceNumber: typing.Optional[int] = None
    image: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentDocumentType:
    type: typing.Optional[str] = None
    shippingDocumentDisposition: typing.Optional[str] = None
    imageType: typing.Optional[str] = None
    resolution: typing.Optional[int] = None
    copiesToPrint: typing.Optional[int] = None
    parts: typing.Optional[typing.List[PartType]] = jstruct.JList[PartType]


@attr.s(auto_attribs=True)
class CurrencyExchangeRateType:
    rate: typing.Optional[float] = None
    fromCurrency: typing.Optional[str] = None
    intoCurrency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FreightDiscountType:
    amount: typing.Optional[float] = None
    rateDiscountType: typing.Optional[str] = None
    percent: typing.Optional[float] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRateDetailSurchargeType:
    amount: typing.Optional[typing.Union[float, str]] = None
    surchargeType: typing.Optional[str] = None
    level: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TaxType:
    amount: typing.Optional[float] = None
    level: typing.Optional[str] = None
    description: typing.Optional[str] = None
    type: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRateDetailType:
    rateZone: typing.Optional[str] = None
    ratedWeightMethod: typing.Optional[str] = None
    totalDutiesTaxesAndFees: typing.Optional[float] = None
    pricingCode: typing.Optional[str] = None
    totalFreightDiscounts: typing.Optional[float] = None
    totalTaxes: typing.Optional[float] = None
    totalDutiesAndTaxes: typing.Optional[float] = None
    totalAncillaryFeesAndTaxes: typing.Optional[float] = None
    taxes: typing.Optional[typing.List[TaxType]] = jstruct.JList[TaxType]
    totalRebates: typing.Optional[float] = None
    fuelSurchargePercent: typing.Optional[float] = None
    currencyExchangeRate: typing.Optional[CurrencyExchangeRateType] = jstruct.JStruct[CurrencyExchangeRateType]
    totalNetFreight: typing.Optional[float] = None
    totalNetFedExCharge: typing.Optional[float] = None
    shipmentLegRateDetails: typing.Optional[typing.List[typing.Any]] = None
    dimDivisor: typing.Optional[int] = None
    rateType: typing.Optional[str] = None
    surcharges: typing.Optional[typing.List[ShipmentRateDetailSurchargeType]] = jstruct.JList[ShipmentRateDetailSurchargeType]
    totalSurcharges: typing.Optional[float] = None
    totalBillingWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    freightDiscounts: typing.Optional[typing.List[FreightDiscountType]] = jstruct.JList[FreightDiscountType]
    rateScale: typing.Optional[str] = None
    totalNetCharge: typing.Optional[float] = None
    totalBaseCharge: typing.Optional[float] = None
    totalNetChargeWithDutiesAndTaxes: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRatingType:
    actualRateType: typing.Optional[str] = None
    shipmentRateDetails: typing.Optional[typing.List[ShipmentRateDetailType]] = jstruct.JList[ShipmentRateDetailType]


@attr.s(auto_attribs=True)
class CompletedShipmentDetailType:
    completedPackageDetails: typing.Optional[typing.List[CompletedPackageDetailType]] = jstruct.JList[CompletedPackageDetailType]
    operationalDetail: typing.Optional[CompletedShipmentDetailOperationalDetailType] = jstruct.JStruct[CompletedShipmentDetailOperationalDetailType]
    carrierCode: typing.Optional[str] = None
    completedHoldAtLocationDetail: typing.Optional[CompletedHoldAtLocationDetailType] = jstruct.JStruct[CompletedHoldAtLocationDetailType]
    completedEtdDetail: typing.Optional[CompletedEtdDetailType] = jstruct.JStruct[CompletedEtdDetailType]
    packagingDescription: typing.Optional[str] = None
    masterTrackingId: typing.Optional[TrackingIDType] = jstruct.JStruct[TrackingIDType]
    serviceDescription: typing.Optional[ServiceDescriptionType] = jstruct.JStruct[ServiceDescriptionType]
    usDomestic: typing.Optional[bool] = None
    hazardousShipmentDetail: typing.Optional[HazardousShipmentDetailType] = jstruct.JStruct[HazardousShipmentDetailType]
    shipmentRating: typing.Optional[ShipmentRatingType] = jstruct.JStruct[ShipmentRatingType]
    documentRequirements: typing.Optional[DocumentRequirementsType] = jstruct.JStruct[DocumentRequirementsType]
    exportComplianceStatement: typing.Optional[str] = None
    accessDetail: typing.Optional[AccessDetailType] = jstruct.JStruct[AccessDetailType]
    shipmentDocuments: typing.Optional[typing.List[ShipmentDocumentType]] = jstruct.JList[ShipmentDocumentType]


@attr.s(auto_attribs=True)
class CustomerReferenceType:
    customerReferenceType: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DocumentType:
    contentKey: typing.Optional[str] = None
    copiesToPrint: typing.Optional[int] = None
    contentType: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    docType: typing.Optional[str] = None
    alerts: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]
    encodedLabel: typing.Optional[str] = None
    url: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TransactionDetailType:
    transactionDetails: typing.Optional[str] = None
    transactionId: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PieceResponseType:
    netChargeAmount: typing.Optional[float] = None
    transactionDetails: typing.Optional[typing.List[TransactionDetailType]] = jstruct.JList[TransactionDetailType]
    packageDocuments: typing.Optional[typing.List[DocumentType]] = jstruct.JList[DocumentType]
    acceptanceTrackingNumber: typing.Optional[str] = None
    serviceCategory: typing.Optional[str] = None
    listCustomerTotalCharge: typing.Optional[str] = None
    deliveryTimestamp: typing.Optional[str] = None
    trackingIdType: typing.Optional[str] = None
    additionalChargesDiscount: typing.Optional[float] = None
    netListRateAmount: typing.Optional[float] = None
    baseRateAmount: typing.Optional[float] = None
    packageSequenceNumber: typing.Optional[int] = None
    netDiscountAmount: typing.Optional[float] = None
    codcollectionAmount: typing.Optional[float] = None
    masterTrackingNumber: typing.Optional[str] = None
    acceptanceType: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    successful: typing.Optional[bool] = None
    customerReferences: typing.Optional[typing.List[CustomerReferenceType]] = jstruct.JList[CustomerReferenceType]
    netRateAmount: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParameterType:
    id: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdvisoryType:
    code: typing.Optional[str] = None
    text: typing.Optional[str] = None
    parameters: typing.Optional[typing.List[ParameterType]] = jstruct.JList[ParameterType]
    localizedText: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WaiverType:
    advisories: typing.Optional[typing.List[AdvisoryType]] = jstruct.JList[AdvisoryType]
    description: typing.Optional[str] = None
    id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ProhibitionType:
    derivedHarmonizedCode: typing.Optional[str] = None
    advisory: typing.Optional[AdvisoryType] = jstruct.JStruct[AdvisoryType]
    commodityIndex: typing.Optional[int] = None
    source: typing.Optional[str] = None
    categories: typing.Optional[typing.List[str]] = None
    type: typing.Optional[str] = None
    waiver: typing.Optional[WaiverType] = jstruct.JStruct[WaiverType]
    status: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RegulatoryAdvisoryType:
    prohibitions: typing.Optional[typing.List[ProhibitionType]] = jstruct.JList[ProhibitionType]


@attr.s(auto_attribs=True)
class ShipmentAdvisoryDetailsType:
    regulatoryAdvisory: typing.Optional[RegulatoryAdvisoryType] = jstruct.JStruct[RegulatoryAdvisoryType]


@attr.s(auto_attribs=True)
class TransactionShipmentType:
    serviceType: typing.Optional[str] = None
    shipDatestamp: typing.Optional[str] = None
    serviceCategory: typing.Optional[str] = None
    shipmentDocuments: typing.Optional[typing.List[DocumentType]] = jstruct.JList[DocumentType]
    pieceResponses: typing.Optional[typing.List[PieceResponseType]] = jstruct.JList[PieceResponseType]
    serviceName: typing.Optional[str] = None
    alerts: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]
    completedShipmentDetail: typing.Optional[CompletedShipmentDetailType] = jstruct.JStruct[CompletedShipmentDetailType]
    shipmentAdvisoryDetails: typing.Optional[ShipmentAdvisoryDetailsType] = jstruct.JStruct[ShipmentAdvisoryDetailsType]
    masterTrackingNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OutputType:
    transactionShipments: typing.Optional[typing.List[TransactionShipmentType]] = jstruct.JList[TransactionShipmentType]
    alerts: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]
    jobId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingResponseType:
    transactionId: typing.Optional[str] = None
    customerTransactionId: typing.Optional[str] = None
    output: typing.Optional[OutputType] = jstruct.JStruct[OutputType]
