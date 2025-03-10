import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CustomerClassificationType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None
    TransactionIdentifier: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestType:
    RequestOption: typing.Optional[str] = None
    SubVersion: typing.Optional[str] = None
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class AlternateDeliveryAddressAddressType:
    AddressLine: typing.Optional[str] = None
    City: typing.Optional[str] = None
    StateProvinceCode: typing.Optional[str] = None
    PostalCode: typing.Optional[int] = None
    CountryCode: typing.Optional[str] = None
    ResidentialAddressIndicator: typing.Optional[str] = None
    POBoxIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AlternateDeliveryAddressType:
    Name: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]


@attr.s(auto_attribs=True)
class PickupType:
    Date: typing.Optional[str] = None
    Time: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryTimeInformationType:
    PackageBillType: typing.Optional[str] = None
    Pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
    ReturnContractServices: typing.Optional[typing.List[CustomerClassificationType]] = jstruct.JList[CustomerClassificationType]
    MasterCartonIndicator: typing.Optional[str] = None
    WWEShipmentIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FRSPaymentInformationAddressType:
    PostalCode: typing.Optional[int] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FRSPaymentInformationType:
    Type: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    AccountNumber: typing.Optional[str] = None
    Address: typing.Optional[FRSPaymentInformationAddressType] = jstruct.JStruct[FRSPaymentInformationAddressType]


@attr.s(auto_attribs=True)
class AdjustedHeightType:
    Value: typing.Optional[int] = None
    UnitOfMeasurement: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]


@attr.s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    Length: typing.Optional[int] = None
    Width: typing.Optional[int] = None
    Height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class HandlingUnitsType:
    Quantity: typing.Optional[int] = None
    Type: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class FreightDensityInfoType:
    AdjustedHeightIndicator: typing.Optional[str] = None
    AdjustedHeight: typing.Optional[AdjustedHeightType] = jstruct.JStruct[AdjustedHeightType]
    HandlingUnits: typing.Optional[HandlingUnitsType] = jstruct.JStruct[HandlingUnitsType]


@attr.s(auto_attribs=True)
class FreightShipmentInformationType:
    FreightDensityInfo: typing.Optional[FreightDensityInfoType] = jstruct.JStruct[FreightDensityInfoType]
    DensityEligibleIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InvoiceLineTotalType:
    CurrencyCode: typing.Optional[str] = None
    MonetaryValue: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class NmfcType:
    PrimeCode: typing.Optional[str] = None
    SubCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityType:
    FreightClass: typing.Optional[str] = None
    NMFC: typing.Optional[NmfcType] = jstruct.JStruct[NmfcType]


@attr.s(auto_attribs=True)
class WeightType:
    UnitOfMeasurement: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    Weight: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CodType:
    CODFundsCode: typing.Optional[int] = None
    CODAmount: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]


@attr.s(auto_attribs=True)
class DeliveryConfirmationType:
    DCISType: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DryIceType:
    RegulationSet: typing.Optional[str] = None
    DryIceWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    MedicalUseIndicator: typing.Optional[str] = None
    AuditRequired: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HazMatChemicalRecordType:
    ChemicalRecordIdentifier: typing.Optional[str] = None
    ClassDivisionNumber: typing.Optional[str] = None
    IDNumber: typing.Optional[str] = None
    TransportationMode: typing.Optional[str] = None
    RegulationSet: typing.Optional[str] = None
    EmergencyPhone: typing.Optional[str] = None
    EmergencyContact: typing.Optional[str] = None
    ReportableQuantity: typing.Optional[str] = None
    SubRiskClass: typing.Optional[str] = None
    PackagingGroupType: typing.Optional[str] = None
    PackagingInstructionCode: typing.Optional[str] = None
    Quantity: typing.Optional[str] = None
    UOM: typing.Optional[str] = None
    ProperShippingName: typing.Optional[str] = None
    TechnicalName: typing.Optional[str] = None
    AdditionalDescription: typing.Optional[str] = None
    PackagingType: typing.Optional[str] = None
    HazardLabelRequired: typing.Optional[str] = None
    PackagingTypeQuantity: typing.Optional[str] = None
    CommodityRegulatedLevelCode: typing.Optional[str] = None
    TransportCategory: typing.Optional[str] = None
    TunnelRestrictionCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HazMatType:
    PackageIdentifier: typing.Optional[str] = None
    QValue: typing.Optional[str] = None
    OverPackedIndicator: typing.Optional[str] = None
    AllPackedInOneIndicator: typing.Optional[str] = None
    HazMatChemicalRecord: typing.Optional[HazMatChemicalRecordType] = jstruct.JStruct[HazMatChemicalRecordType]


@attr.s(auto_attribs=True)
class PackageServiceOptionsType:
    DeliveryConfirmation: typing.Optional[DeliveryConfirmationType] = jstruct.JStruct[DeliveryConfirmationType]
    AccessPointCOD: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    COD: typing.Optional[CodType] = jstruct.JStruct[CodType]
    DeclaredValue: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    ShipperDeclaredValue: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    ShipperReleaseIndicator: typing.Optional[str] = None
    ProactiveIndicator: typing.Optional[str] = None
    RefrigerationIndicator: typing.Optional[str] = None
    UPSPremiumCareIndicator: typing.Optional[str] = None
    HazMat: typing.Optional[HazMatType] = jstruct.JStruct[HazMatType]
    DryIce: typing.Optional[DryIceType] = jstruct.JStruct[DryIceType]


@attr.s(auto_attribs=True)
class UPSPremierType:
    Category: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageType:
    PackagingType: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    DimWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    PackageWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    Commodity: typing.Optional[CommodityType] = jstruct.JStruct[CommodityType]
    LargePackageIndicator: typing.Optional[str] = None
    PackageServiceOptions: typing.Optional[PackageServiceOptionsType] = jstruct.JStruct[PackageServiceOptionsType]
    AdditionalHandlingIndicator: typing.Optional[str] = None
    UPSPremier: typing.Optional[UPSPremierType] = jstruct.JStruct[UPSPremierType]
    OversizeIndicator: typing.Optional[str] = None
    MinimumBillableWeightIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BillReceiverAddressType:
    PostalCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BillReceiverType:
    AccountNumber: typing.Optional[str] = None
    Address: typing.Optional[BillReceiverAddressType] = jstruct.JStruct[BillReceiverAddressType]


@attr.s(auto_attribs=True)
class BillShipperType:
    AccountNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BillThirdPartyType:
    AccountNumber: typing.Optional[str] = None
    Address: typing.Optional[FRSPaymentInformationAddressType] = jstruct.JStruct[FRSPaymentInformationAddressType]


@attr.s(auto_attribs=True)
class ShipmentChargeType:
    Type: typing.Optional[str] = None
    BillShipper: typing.Optional[BillShipperType] = jstruct.JStruct[BillShipperType]
    BillReceiver: typing.Optional[BillReceiverType] = jstruct.JStruct[BillReceiverType]
    BillThirdParty: typing.Optional[BillThirdPartyType] = jstruct.JStruct[BillThirdPartyType]
    ConsigneeBilledIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PaymentDetailsType:
    ShipmentCharge: typing.Optional[ShipmentChargeType] = jstruct.JStruct[ShipmentChargeType]
    SplitDutyVATIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PromotionalDiscountInformationType:
    PromoCode: typing.Optional[str] = None
    PromoAliasCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipFromAddressType:
    AddressLine: typing.Optional[str] = None
    City: typing.Optional[str] = None
    StateProvinceCode: typing.Optional[str] = None
    PostalCode: typing.Optional[int] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipType:
    Name: typing.Optional[str] = None
    AttentionName: typing.Optional[str] = None
    Address: typing.Optional[ShipFromAddressType] = jstruct.JStruct[ShipFromAddressType]
    ShipperNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipToType:
    Name: typing.Optional[str] = None
    AttentionName: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]


@attr.s(auto_attribs=True)
class ShipmentRatingOptionsType:
    NegotiatedRatesIndicator: typing.Optional[str] = None
    FRSShipmentIndicator: typing.Optional[str] = None
    RateChartIndicator: typing.Optional[str] = None
    UserLevelDiscountIndicator: typing.Optional[str] = None
    TPFCNegotiatedRatesIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryOptionsType:
    LiftGateAtDeliveryIndicator: typing.Optional[str] = None
    DropOffAtUPSFacilityIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupOptionsType:
    LiftGateAtPickupIndicator: typing.Optional[str] = None
    HoldForPickupIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RestrictedArticlesType:
    AlcoholicBeveragesIndicator: typing.Optional[str] = None
    DiagnosticSpecimensIndicator: typing.Optional[str] = None
    PerishablesIndicator: typing.Optional[str] = None
    PlantsIndicator: typing.Optional[str] = None
    SeedsIndicator: typing.Optional[str] = None
    SpecialExceptionsIndicator: typing.Optional[str] = None
    TobaccoIndicator: typing.Optional[str] = None
    ECigarettesIndicator: typing.Optional[str] = None
    HempCBDIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentServiceOptionsType:
    SaturdayPickupIndicator: typing.Optional[str] = None
    SaturdayDeliveryIndicator: typing.Optional[str] = None
    SundayDeliveryIndicator: typing.Optional[str] = None
    AvailableServicesOption: typing.Optional[str] = None
    AccessPointCOD: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    DeliverToAddresseeOnlyIndicator: typing.Optional[str] = None
    DirectDeliveryOnlyIndicator: typing.Optional[str] = None
    COD: typing.Optional[CodType] = jstruct.JStruct[CodType]
    DeliveryConfirmation: typing.Optional[DeliveryConfirmationType] = jstruct.JStruct[DeliveryConfirmationType]
    ReturnOfDocumentIndicator: typing.Optional[str] = None
    UPScarbonneutralIndicator: typing.Optional[str] = None
    CertificateOfOriginIndicator: typing.Optional[str] = None
    PickupOptions: typing.Optional[PickupOptionsType] = jstruct.JStruct[PickupOptionsType]
    DeliveryOptions: typing.Optional[DeliveryOptionsType] = jstruct.JStruct[DeliveryOptionsType]
    RestrictedArticles: typing.Optional[RestrictedArticlesType] = jstruct.JStruct[RestrictedArticlesType]
    ShipperExportDeclarationIndicator: typing.Optional[str] = None
    CommercialInvoiceRemovalIndicator: typing.Optional[str] = None
    ImportControl: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    ReturnService: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    SDLShipmentIndicator: typing.Optional[str] = None
    EPRAIndicator: typing.Optional[str] = None
    InsideDelivery: typing.Optional[str] = None
    ItemDisposalIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentType:
    OriginRecordTransactionTimestamp: typing.Optional[str] = None
    Shipper: typing.Optional[ShipType] = jstruct.JStruct[ShipType]
    ShipTo: typing.Optional[ShipToType] = jstruct.JStruct[ShipToType]
    ShipFrom: typing.Optional[ShipType] = jstruct.JStruct[ShipType]
    AlternateDeliveryAddress: typing.Optional[AlternateDeliveryAddressType] = jstruct.JStruct[AlternateDeliveryAddressType]
    ShipmentIndicatorType: typing.Optional[typing.List[CustomerClassificationType]] = jstruct.JList[CustomerClassificationType]
    PaymentDetails: typing.Optional[PaymentDetailsType] = jstruct.JStruct[PaymentDetailsType]
    FRSPaymentInformation: typing.Optional[FRSPaymentInformationType] = jstruct.JStruct[FRSPaymentInformationType]
    FreightShipmentInformation: typing.Optional[FreightShipmentInformationType] = jstruct.JStruct[FreightShipmentInformationType]
    GoodsNotInFreeCirculationIndicator: typing.Optional[str] = None
    Service: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    NumOfPieces: typing.Optional[int] = None
    ShipmentTotalWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    DocumentsOnlyIndicator: typing.Optional[str] = None
    Package: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    ShipmentServiceOptions: typing.Optional[ShipmentServiceOptionsType] = jstruct.JStruct[ShipmentServiceOptionsType]
    ShipmentRatingOptions: typing.Optional[ShipmentRatingOptionsType] = jstruct.JStruct[ShipmentRatingOptionsType]
    InvoiceLineTotal: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    RatingMethodRequestedIndicator: typing.Optional[str] = None
    TaxInformationIndicator: typing.Optional[str] = None
    PromotionalDiscountInformation: typing.Optional[PromotionalDiscountInformationType] = jstruct.JStruct[PromotionalDiscountInformationType]
    DeliveryTimeInformation: typing.Optional[DeliveryTimeInformationType] = jstruct.JStruct[DeliveryTimeInformationType]


@attr.s(auto_attribs=True)
class RateRequestType:
    Request: typing.Optional[RequestType] = jstruct.JStruct[RequestType]
    PickupType: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    CustomerClassification: typing.Optional[CustomerClassificationType] = jstruct.JStruct[CustomerClassificationType]
    Shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]


@attr.s(auto_attribs=True)
class RatingRequestType:
    RateRequest: typing.Optional[RateRequestType] = jstruct.JStruct[RateRequestType]
