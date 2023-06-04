from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CustomerClassificationType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None
    TransactionIdentifier: Optional[str] = None


@s(auto_attribs=True)
class RequestType:
    RequestOption: Optional[str] = None
    SubVersion: Optional[str] = None
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class AlternateDeliveryAddressAddressType:
    AddressLine: Optional[str] = None
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    PostalCode: Optional[int] = None
    CountryCode: Optional[str] = None
    ResidentialAddressIndicator: Optional[str] = None
    POBoxIndicator: Optional[str] = None


@s(auto_attribs=True)
class AlternateDeliveryAddressType:
    Name: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]


@s(auto_attribs=True)
class PickupType:
    Date: Optional[str] = None
    Time: Optional[str] = None


@s(auto_attribs=True)
class DeliveryTimeInformationType:
    PackageBillType: Optional[str] = None
    Pickup: Optional[PickupType] = JStruct[PickupType]
    ReturnContractServices: List[CustomerClassificationType] = JList[CustomerClassificationType]
    MasterCartonIndicator: Optional[str] = None
    WWEShipmentIndicator: Optional[str] = None


@s(auto_attribs=True)
class FRSPaymentInformationAddressType:
    PostalCode: Optional[int] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class FRSPaymentInformationType:
    Type: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    AccountNumber: Optional[str] = None
    Address: Optional[FRSPaymentInformationAddressType] = JStruct[FRSPaymentInformationAddressType]


@s(auto_attribs=True)
class AdjustedHeightType:
    Value: Optional[int] = None
    UnitOfMeasurement: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]


@s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    Length: Optional[int] = None
    Width: Optional[int] = None
    Height: Optional[int] = None


@s(auto_attribs=True)
class HandlingUnitsType:
    Quantity: Optional[int] = None
    Type: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]


@s(auto_attribs=True)
class FreightDensityInfoType:
    AdjustedHeightIndicator: Optional[str] = None
    AdjustedHeight: Optional[AdjustedHeightType] = JStruct[AdjustedHeightType]
    HandlingUnits: Optional[HandlingUnitsType] = JStruct[HandlingUnitsType]


@s(auto_attribs=True)
class FreightShipmentInformationType:
    FreightDensityInfo: Optional[FreightDensityInfoType] = JStruct[FreightDensityInfoType]
    DensityEligibleIndicator: Optional[str] = None


@s(auto_attribs=True)
class InvoiceLineTotalType:
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[int] = None


@s(auto_attribs=True)
class NmfcType:
    PrimeCode: Optional[str] = None
    SubCode: Optional[str] = None


@s(auto_attribs=True)
class CommodityType:
    FreightClass: Optional[str] = None
    NMFC: Optional[NmfcType] = JStruct[NmfcType]


@s(auto_attribs=True)
class WeightType:
    UnitOfMeasurement: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    Weight: Optional[int] = None


@s(auto_attribs=True)
class CodType:
    CODFundsCode: Optional[int] = None
    CODAmount: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]


@s(auto_attribs=True)
class DeliveryConfirmationType:
    DCISType: Optional[int] = None


@s(auto_attribs=True)
class DryIceType:
    RegulationSet: Optional[str] = None
    DryIceWeight: Optional[WeightType] = JStruct[WeightType]
    MedicalUseIndicator: Optional[str] = None
    AuditRequired: Optional[str] = None


@s(auto_attribs=True)
class HazMatChemicalRecordType:
    ChemicalRecordIdentifier: Optional[str] = None
    ClassDivisionNumber: Optional[str] = None
    IDNumber: Optional[str] = None
    TransportationMode: Optional[str] = None
    RegulationSet: Optional[str] = None
    EmergencyPhone: Optional[str] = None
    EmergencyContact: Optional[str] = None
    ReportableQuantity: Optional[str] = None
    SubRiskClass: Optional[str] = None
    PackagingGroupType: Optional[str] = None
    PackagingInstructionCode: Optional[str] = None
    Quantity: Optional[str] = None
    UOM: Optional[str] = None
    ProperShippingName: Optional[str] = None
    TechnicalName: Optional[str] = None
    AdditionalDescription: Optional[str] = None
    PackagingType: Optional[str] = None
    HazardLabelRequired: Optional[str] = None
    PackagingTypeQuantity: Optional[str] = None
    CommodityRegulatedLevelCode: Optional[str] = None
    TransportCategory: Optional[str] = None
    TunnelRestrictionCode: Optional[str] = None


@s(auto_attribs=True)
class HazMatType:
    PackageIdentifier: Optional[str] = None
    QValue: Optional[str] = None
    OverPackedIndicator: Optional[str] = None
    AllPackedInOneIndicator: Optional[str] = None
    HazMatChemicalRecord: Optional[HazMatChemicalRecordType] = JStruct[HazMatChemicalRecordType]


@s(auto_attribs=True)
class PackageServiceOptionsType:
    DeliveryConfirmation: Optional[DeliveryConfirmationType] = JStruct[DeliveryConfirmationType]
    AccessPointCOD: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    COD: Optional[CodType] = JStruct[CodType]
    DeclaredValue: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    ShipperDeclaredValue: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    ShipperReleaseIndicator: Optional[str] = None
    ProactiveIndicator: Optional[str] = None
    RefrigerationIndicator: Optional[str] = None
    UPSPremiumCareIndicator: Optional[str] = None
    HazMat: Optional[HazMatType] = JStruct[HazMatType]
    DryIce: Optional[DryIceType] = JStruct[DryIceType]


@s(auto_attribs=True)
class UPSPremierType:
    Category: Optional[str] = None


@s(auto_attribs=True)
class PackageType:
    PackagingType: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    DimWeight: Optional[WeightType] = JStruct[WeightType]
    PackageWeight: Optional[WeightType] = JStruct[WeightType]
    Commodity: Optional[CommodityType] = JStruct[CommodityType]
    LargePackageIndicator: Optional[str] = None
    PackageServiceOptions: Optional[PackageServiceOptionsType] = JStruct[PackageServiceOptionsType]
    AdditionalHandlingIndicator: Optional[str] = None
    UPSPremier: Optional[UPSPremierType] = JStruct[UPSPremierType]
    OversizeIndicator: Optional[str] = None
    MinimumBillableWeightIndicator: Optional[str] = None


@s(auto_attribs=True)
class BillReceiverAddressType:
    PostalCode: Optional[int] = None


@s(auto_attribs=True)
class BillReceiverType:
    AccountNumber: Optional[str] = None
    Address: Optional[BillReceiverAddressType] = JStruct[BillReceiverAddressType]


@s(auto_attribs=True)
class BillShipperType:
    AccountNumber: Optional[str] = None


@s(auto_attribs=True)
class BillThirdPartyType:
    AccountNumber: Optional[str] = None
    Address: Optional[FRSPaymentInformationAddressType] = JStruct[FRSPaymentInformationAddressType]


@s(auto_attribs=True)
class ShipmentChargeType:
    Type: Optional[str] = None
    BillShipper: Optional[BillShipperType] = JStruct[BillShipperType]
    BillReceiver: Optional[BillReceiverType] = JStruct[BillReceiverType]
    BillThirdParty: Optional[BillThirdPartyType] = JStruct[BillThirdPartyType]
    ConsigneeBilledIndicator: Optional[str] = None


@s(auto_attribs=True)
class PaymentDetailsType:
    ShipmentCharge: Optional[ShipmentChargeType] = JStruct[ShipmentChargeType]
    SplitDutyVATIndicator: Optional[str] = None


@s(auto_attribs=True)
class PromotionalDiscountInformationType:
    PromoCode: Optional[str] = None
    PromoAliasCode: Optional[str] = None


@s(auto_attribs=True)
class ShipFromAddressType:
    AddressLine: Optional[str] = None
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    PostalCode: Optional[int] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class ShipType:
    Name: Optional[str] = None
    AttentionName: Optional[str] = None
    Address: Optional[ShipFromAddressType] = JStruct[ShipFromAddressType]
    ShipperNumber: Optional[str] = None


@s(auto_attribs=True)
class ShipToType:
    Name: Optional[str] = None
    AttentionName: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]


@s(auto_attribs=True)
class ShipmentRatingOptionsType:
    NegotiatedRatesIndicator: Optional[str] = None
    FRSShipmentIndicator: Optional[str] = None
    RateChartIndicator: Optional[str] = None
    UserLevelDiscountIndicator: Optional[str] = None
    TPFCNegotiatedRatesIndicator: Optional[str] = None


@s(auto_attribs=True)
class DeliveryOptionsType:
    LiftGateAtDeliveryIndicator: Optional[str] = None
    DropOffAtUPSFacilityIndicator: Optional[str] = None


@s(auto_attribs=True)
class PickupOptionsType:
    LiftGateAtPickupIndicator: Optional[str] = None
    HoldForPickupIndicator: Optional[str] = None


@s(auto_attribs=True)
class RestrictedArticlesType:
    AlcoholicBeveragesIndicator: Optional[str] = None
    DiagnosticSpecimensIndicator: Optional[str] = None
    PerishablesIndicator: Optional[str] = None
    PlantsIndicator: Optional[str] = None
    SeedsIndicator: Optional[str] = None
    SpecialExceptionsIndicator: Optional[str] = None
    TobaccoIndicator: Optional[str] = None
    ECigarettesIndicator: Optional[str] = None
    HempCBDIndicator: Optional[str] = None


@s(auto_attribs=True)
class ShipmentServiceOptionsType:
    SaturdayPickupIndicator: Optional[str] = None
    SaturdayDeliveryIndicator: Optional[str] = None
    SundayDeliveryIndicator: Optional[str] = None
    AvailableServicesOption: Optional[str] = None
    AccessPointCOD: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    DeliverToAddresseeOnlyIndicator: Optional[str] = None
    DirectDeliveryOnlyIndicator: Optional[str] = None
    COD: Optional[CodType] = JStruct[CodType]
    DeliveryConfirmation: Optional[DeliveryConfirmationType] = JStruct[DeliveryConfirmationType]
    ReturnOfDocumentIndicator: Optional[str] = None
    UPScarbonneutralIndicator: Optional[str] = None
    CertificateOfOriginIndicator: Optional[str] = None
    PickupOptions: Optional[PickupOptionsType] = JStruct[PickupOptionsType]
    DeliveryOptions: Optional[DeliveryOptionsType] = JStruct[DeliveryOptionsType]
    RestrictedArticles: Optional[RestrictedArticlesType] = JStruct[RestrictedArticlesType]
    ShipperExportDeclarationIndicator: Optional[str] = None
    CommercialInvoiceRemovalIndicator: Optional[str] = None
    ImportControl: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    ReturnService: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    SDLShipmentIndicator: Optional[str] = None
    EPRAIndicator: Optional[str] = None
    InsideDelivery: Optional[str] = None
    ItemDisposalIndicator: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    OriginRecordTransactionTimestamp: Optional[str] = None
    Shipper: Optional[ShipType] = JStruct[ShipType]
    ShipTo: Optional[ShipToType] = JStruct[ShipToType]
    ShipFrom: Optional[ShipType] = JStruct[ShipType]
    AlternateDeliveryAddress: Optional[AlternateDeliveryAddressType] = JStruct[AlternateDeliveryAddressType]
    ShipmentIndicatorType: List[CustomerClassificationType] = JList[CustomerClassificationType]
    PaymentDetails: Optional[PaymentDetailsType] = JStruct[PaymentDetailsType]
    FRSPaymentInformation: Optional[FRSPaymentInformationType] = JStruct[FRSPaymentInformationType]
    FreightShipmentInformation: Optional[FreightShipmentInformationType] = JStruct[FreightShipmentInformationType]
    GoodsNotInFreeCirculationIndicator: Optional[str] = None
    Service: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    NumOfPieces: Optional[int] = None
    ShipmentTotalWeight: Optional[WeightType] = JStruct[WeightType]
    DocumentsOnlyIndicator: Optional[str] = None
    Package: List[PackageType] = JList[PackageType]
    ShipmentServiceOptions: Optional[ShipmentServiceOptionsType] = JStruct[ShipmentServiceOptionsType]
    ShipmentRatingOptions: Optional[ShipmentRatingOptionsType] = JStruct[ShipmentRatingOptionsType]
    InvoiceLineTotal: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    RatingMethodRequestedIndicator: Optional[str] = None
    TaxInformationIndicator: Optional[str] = None
    PromotionalDiscountInformation: Optional[PromotionalDiscountInformationType] = JStruct[PromotionalDiscountInformationType]
    DeliveryTimeInformation: Optional[DeliveryTimeInformationType] = JStruct[DeliveryTimeInformationType]


@s(auto_attribs=True)
class RateRequestType:
    Request: Optional[RequestType] = JStruct[RequestType]
    PickupType: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    CustomerClassification: Optional[CustomerClassificationType] = JStruct[CustomerClassificationType]
    Shipment: Optional[ShipmentType] = JStruct[ShipmentType]


@s(auto_attribs=True)
class RatingRequestType:
    RateRequest: Optional[RateRequestType] = JStruct[RateRequestType]
