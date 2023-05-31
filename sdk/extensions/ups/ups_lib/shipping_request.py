from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class LabelImageFormatType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class LabelStockSizeType:
    Height: Optional[str] = None
    Width: Optional[str] = None


@s(auto_attribs=True)
class LabelSpecificationType:
    LabelImageFormat: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    HTTPUserAgent: Optional[str] = None
    LabelStockSize: Optional[LabelStockSizeType] = JStruct[LabelStockSizeType]
    Instruction: List[LabelImageFormatType] = JList[LabelImageFormatType]
    CharacterSet: Optional[str] = None


@s(auto_attribs=True)
class ReceiptSpecificationType:
    ImageFormat: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None


@s(auto_attribs=True)
class RequestType:
    SubVersion: Optional[int] = None
    RequestOption: Optional[str] = None
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class AlternateDeliveryAddressAddressType:
    AddressLine: Optional[str] = None
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    PostalCode: Optional[str] = None
    CountryCode: Optional[str] = None
    ResidentialAddressIndicator: Optional[str] = None


@s(auto_attribs=True)
class AlternateDeliveryAddressType:
    Name: Optional[str] = None
    AttentionName: Optional[str] = None
    UPSAccessPointID: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]


@s(auto_attribs=True)
class DGSignatoryInfoType:
    Name: Optional[str] = None
    Title: Optional[str] = None
    Place: Optional[str] = None
    Date: Optional[str] = None
    ShipperDeclaration: Optional[str] = None
    UploadOnlyIndicator: Optional[str] = None


@s(auto_attribs=True)
class FRSPaymentInformationAddressType:
    PostalCode: Optional[int] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class FRSPaymentInformationType:
    Type: Optional[str] = None
    AccountNumber: Optional[str] = None
    Address: Optional[FRSPaymentInformationAddressType] = JStruct[FRSPaymentInformationAddressType]


@s(auto_attribs=True)
class AdjustedHeightType:
    Value: Optional[int] = None
    UnitOfMeasurement: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]


@s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    Length: Optional[int] = None
    Width: Optional[int] = None
    Height: Optional[int] = None


@s(auto_attribs=True)
class HandlingUnitsType:
    Quantity: Optional[int] = None
    Type: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
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
    UnitOfMeasurement: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    Weight: Optional[int] = None


@s(auto_attribs=True)
class HazMatPackageInformationType:
    AllPackedInOneIndicator: Optional[str] = None
    OverPackedIndicator: Optional[str] = None
    QValue: Optional[str] = None
    OuterPackagingType: Optional[str] = None


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
class ReferenceNumberType:
    BarCodeIndicator: Optional[str] = None
    Code: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class HandlingInstructionsType:
    Instruction: Optional[str] = None


@s(auto_attribs=True)
class UPSPremierType:
    Category: Optional[str] = None
    SensorID: Optional[str] = None
    HandlingInstructions: Optional[HandlingInstructionsType] = JStruct[HandlingInstructionsType]


@s(auto_attribs=True)
class PackageType:
    Description: Optional[str] = None
    PalletDescription: Optional[str] = None
    NumOfPieces: Optional[int] = None
    UnitPrice: Optional[str] = None
    Packaging: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    DimWeight: Optional[WeightType] = JStruct[WeightType]
    PackageWeight: Optional[WeightType] = JStruct[WeightType]
    LargePackageIndicator: Optional[str] = None
    ReferenceNumber: Optional[ReferenceNumberType] = JStruct[ReferenceNumberType]
    AdditionalHandlingIndicator: Optional[str] = None
    UPSPremier: Optional[UPSPremierType] = JStruct[UPSPremierType]
    PackageServiceOptions: Optional[PackageServiceOptionsType] = JStruct[PackageServiceOptionsType]
    Commodity: Optional[CommodityType] = JStruct[CommodityType]
    HazMatPackageInformation: Optional[HazMatPackageInformationType] = JStruct[HazMatPackageInformationType]


@s(auto_attribs=True)
class BillReceiverAddressType:
    PostalCode: Optional[int] = None


@s(auto_attribs=True)
class BillReceiverType:
    AccountNumber: Optional[str] = None
    Address: Optional[BillReceiverAddressType] = JStruct[BillReceiverAddressType]


@s(auto_attribs=True)
class CreditCardType:
    Type: Optional[str] = None
    Number: Optional[str] = None
    ExpirationDate: Optional[int] = None
    SecurityCode: Optional[int] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]


@s(auto_attribs=True)
class BillShipperType:
    AccountNumber: Optional[str] = None
    CreditCard: Optional[CreditCardType] = JStruct[CreditCardType]
    AlternatePaymentMethod: Optional[str] = None


@s(auto_attribs=True)
class BillThirdPartyType:
    AccountNumber: Optional[str] = None
    CertifiedElectronicMail: Optional[str] = None
    InterchangeSystemCode: Optional[str] = None
    Address: Optional[FRSPaymentInformationAddressType] = JStruct[FRSPaymentInformationAddressType]


@s(auto_attribs=True)
class ShipmentChargeType:
    Type: Optional[str] = None
    BillShipper: Optional[BillShipperType] = JStruct[BillShipperType]
    BillReceiver: Optional[BillReceiverType] = JStruct[BillReceiverType]
    BillThirdParty: Optional[BillThirdPartyType] = JStruct[BillThirdPartyType]
    ConsigneeBilledIndicator: Optional[str] = None


@s(auto_attribs=True)
class PaymentInformationType:
    ShipmentCharge: Optional[ShipmentChargeType] = JStruct[ShipmentChargeType]
    SplitDutyVATIndicator: Optional[str] = None


@s(auto_attribs=True)
class PromotionalDiscountInformationType:
    PromoCode: Optional[str] = None
    PromoAliasCode: Optional[str] = None


@s(auto_attribs=True)
class ShipFromPhoneType:
    Number: Optional[int] = None


@s(auto_attribs=True)
class VendorInfoType:
    VendorCollectIDTypeCode: Optional[str] = None
    VendorCollectIDNumber: Optional[int] = None
    ConsigneeType: Optional[str] = None


@s(auto_attribs=True)
class ShipFromType:
    Name: Optional[str] = None
    AttentionName: Optional[str] = None
    CompanyDisplayableName: Optional[str] = None
    TaxIdentificationNumber: Optional[int] = None
    TaxId: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    Phone: Optional[ShipFromPhoneType] = JStruct[ShipFromPhoneType]
    FaxNumber: Optional[int] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]
    VendorInfo: Optional[VendorInfoType] = JStruct[VendorInfoType]


@s(auto_attribs=True)
class ShipToPhoneType:
    Number: Optional[str] = None
    Extension: Optional[str] = None


@s(auto_attribs=True)
class ShipToType:
    Name: Optional[str] = None
    AttentionName: Optional[str] = None
    CompanyDisplayableName: Optional[str] = None
    TaxIdentificationNumber: Optional[int] = None
    Phone: Optional[ShipToPhoneType] = JStruct[ShipToPhoneType]
    FaxNumber: Optional[int] = None
    EMailAddress: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]
    LocationID: Optional[str] = None


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
    ImportControl: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    ReturnService: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    SDLShipmentIndicator: Optional[str] = None
    EPRAIndicator: Optional[str] = None
    InsideDelivery: Optional[str] = None
    ItemDisposalIndicator: Optional[str] = None


@s(auto_attribs=True)
class ShipperType:
    Name: Optional[str] = None
    AttentionName: Optional[str] = None
    CompanyDisplayableName: Optional[str] = None
    TaxIdentificationNumber: Optional[int] = None
    Phone: Optional[ShipToPhoneType] = JStruct[ShipToPhoneType]
    ShipperNumber: Optional[str] = None
    FaxNumber: Optional[str] = None
    EMailAddress: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]


@s(auto_attribs=True)
class ShipmentType:
    Description: Optional[str] = None
    ReturnService: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    DocumentsOnlyIndicator: Optional[str] = None
    Shipper: Optional[ShipperType] = JStruct[ShipperType]
    ShipTo: Optional[ShipToType] = JStruct[ShipToType]
    AlternateDeliveryAddress: Optional[AlternateDeliveryAddressType] = JStruct[AlternateDeliveryAddressType]
    ShipFrom: Optional[ShipFromType] = JStruct[ShipFromType]
    PaymentInformation: Optional[PaymentInformationType] = JStruct[PaymentInformationType]
    FRSPaymentInformation: Optional[FRSPaymentInformationType] = JStruct[FRSPaymentInformationType]
    FreightShipmentInformation: Optional[FreightShipmentInformationType] = JStruct[FreightShipmentInformationType]
    GoodsNotInFreeCirculationIndicator: Optional[str] = None
    PromotionalDiscountInformation: Optional[PromotionalDiscountInformationType] = JStruct[PromotionalDiscountInformationType]
    DGSignatoryInfo: Optional[DGSignatoryInfoType] = JStruct[DGSignatoryInfoType]
    ShipmentRatingOptions: Optional[ShipmentRatingOptionsType] = JStruct[ShipmentRatingOptionsType]
    MovementReferenceNumber: Optional[str] = None
    ReferenceNumber: Optional[ReferenceNumberType] = JStruct[ReferenceNumberType]
    Service: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    InvoiceLineTotal: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    NumOfPiecesInShipment: Optional[int] = None
    USPSEndorsement: Optional[str] = None
    MILabelCN22Indicator: Optional[str] = None
    SubClassification: Optional[str] = None
    CostCenter: Optional[str] = None
    CostCenterBarcodeIndicator: Optional[str] = None
    PackageID: Optional[str] = None
    PackageIDBarcodeIndicator: Optional[str] = None
    IrregularIndicator: Optional[str] = None
    ShipmentIndicationType: List[LabelImageFormatType] = JList[LabelImageFormatType]
    MIDualReturnShipmentKey: Optional[str] = None
    RatingMethodRequestedIndicator: Optional[str] = None
    TaxInformationIndicator: Optional[str] = None
    ShipmentServiceOptions: Optional[ShipmentServiceOptionsType] = JStruct[ShipmentServiceOptionsType]
    Locale: Optional[str] = None
    ShipmentValueThresholdCode: Optional[str] = None
    MasterCartonID: Optional[str] = None
    MasterCartonIndicator: Optional[str] = None
    BarCodeImageIndicator: Optional[str] = None
    BarCodeAndLabelIndicator: Optional[str] = None
    ShipmentDate: Optional[int] = None
    Package: Optional[PackageType] = JStruct[PackageType]


@s(auto_attribs=True)
class ShipmentRequestType:
    Request: Optional[RequestType] = JStruct[RequestType]
    Shipment: Optional[ShipmentType] = JStruct[ShipmentType]
    LabelSpecification: Optional[LabelSpecificationType] = JStruct[LabelSpecificationType]
    ReceiptSpecification: Optional[ReceiptSpecificationType] = JStruct[ReceiptSpecificationType]


@s(auto_attribs=True)
class ShippingRequestType:
    ShipmentRequest: Optional[ShipmentRequestType] = JStruct[ShipmentRequestType]
