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
    Town: Optional[str] = None


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
    Weight: Optional[str] = None


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
class PackageServiceOptionsDeliveryConfirmationType:
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
class MailType:
    EMailAddress: Optional[str] = None
    UndeliverableEMailAddress: Optional[str] = None
    FromEMailAddress: Optional[str] = None
    FromName: Optional[str] = None
    Memo: Optional[str] = None
    Subject: Optional[str] = None
    SubjectCode: Optional[str] = None


@s(auto_attribs=True)
class PackageServiceOptionsNotificationType:
    NotificationCode: Optional[int] = None
    Email: Optional[MailType] = JStruct[MailType]


@s(auto_attribs=True)
class PackageServiceOptionsType:
    DeliveryConfirmation: Optional[PackageServiceOptionsDeliveryConfirmationType] = JStruct[PackageServiceOptionsDeliveryConfirmationType]
    DeclaredValue: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    COD: Optional[CodType] = JStruct[CodType]
    AccessPointCOD: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    ShipperReleaseIndicator: Optional[str] = None
    Notification: Optional[PackageServiceOptionsNotificationType] = JStruct[PackageServiceOptionsNotificationType]
    HazMat: Optional[HazMatType] = JStruct[HazMatType]
    DryIce: Optional[DryIceType] = JStruct[DryIceType]
    UPSPremiumCareIndicator: Optional[str] = None
    ProactiveIndicator: Optional[str] = None
    PackageIdentifier: Optional[str] = None
    ClinicalTrialsID: Optional[str] = None
    RefrigerationIndicator: Optional[str] = None


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
    ShipmentCharge: List[ShipmentChargeType] = JList[ShipmentChargeType]
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
class ShipmentServiceOptionsDeliveryConfirmationType:
    DCISType: Optional[int] = None
    DCISNumber: Optional[int] = None


@s(auto_attribs=True)
class BlanketPeriodType:
    BeginDate: Optional[str] = None
    EndDate: Optional[str] = None


@s(auto_attribs=True)
class CN22ContentType:
    CN22ContentQuantity: Optional[str] = None
    CN22ContentDescription: Optional[str] = None
    CN22ContentWeight: Optional[WeightType] = JStruct[WeightType]
    CN22ContentTotalValue: Optional[str] = None
    CN22ContentCurrencyCode: Optional[str] = None
    CN22ContentCountryOfOrigin: Optional[str] = None
    CN22ContentTariffNumber: Optional[str] = None


@s(auto_attribs=True)
class CN22FormType:
    LabelSize: Optional[str] = None
    PrintsPerPage: Optional[str] = None
    LabelPrintType: Optional[str] = None
    CN22Type: Optional[str] = None
    CN22OtherDescription: Optional[str] = None
    FoldHereText: Optional[str] = None
    CN22Content: Optional[CN22ContentType] = JStruct[CN22ContentType]


@s(auto_attribs=True)
class ForwardAgentType:
    CompanyName: Optional[str] = None
    TaxIdentificationNumber: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]


@s(auto_attribs=True)
class IntermediateConsigneeType:
    CompanyName: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]


@s(auto_attribs=True)
class ProducerType:
    Option: Optional[str] = None
    CompanyName: Optional[str] = None
    TaxIdentificationNumber: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]
    AttentionName: Optional[str] = None
    Phone: Optional[ShipToPhoneType] = JStruct[ShipToPhoneType]
    EMailAddress: Optional[str] = None
    Name: Optional[str] = None


@s(auto_attribs=True)
class UltimateConsigneeType:
    CompanyName: Optional[str] = None
    Address: Optional[AlternateDeliveryAddressAddressType] = JStruct[AlternateDeliveryAddressAddressType]
    UltimateConsigneeType: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]


@s(auto_attribs=True)
class ContactsType:
    ForwardAgent: Optional[ForwardAgentType] = JStruct[ForwardAgentType]
    UltimateConsignee: Optional[UltimateConsigneeType] = JStruct[UltimateConsigneeType]
    IntermediateConsignee: Optional[IntermediateConsigneeType] = JStruct[IntermediateConsigneeType]
    Producer: Optional[ProducerType] = JStruct[ProducerType]
    SoldTo: Optional[ProducerType] = JStruct[ProducerType]


@s(auto_attribs=True)
class DiscountType:
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class ShipperFiledType:
    Code: Optional[str] = None
    Description: Optional[str] = None
    PreDepartureITNNumber: Optional[str] = None
    ExemptionLegend: Optional[str] = None
    EEIShipmentReferenceNumber: Optional[str] = None


@s(auto_attribs=True)
class UPSFiledType:
    POA: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]


@s(auto_attribs=True)
class EEIFilingOptionType:
    Code: Optional[str] = None
    EMailAddress: Optional[str] = None
    Description: Optional[str] = None
    UPSFiled: Optional[UPSFiledType] = JStruct[UPSFiledType]
    ShipperFiled: Optional[ShipperFiledType] = JStruct[ShipperFiledType]


@s(auto_attribs=True)
class OtherChargesType:
    MonetaryValue: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class DDTCInformationType:
    ITARExemptionNumber: Optional[str] = None
    USMLCategoryCode: Optional[str] = None
    EligiblePartyIndicator: Optional[str] = None
    RegistrationNumber: Optional[str] = None
    Quantity: Optional[str] = None
    UnitOfMeasurement: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    SignificantMilitaryEquipmentIndicator: Optional[str] = None
    ACMNumber: Optional[str] = None


@s(auto_attribs=True)
class LicenseType:
    Number: Optional[str] = None
    Code: Optional[str] = None
    LicenseLineValue: Optional[str] = None
    ECCNNumber: Optional[str] = None


@s(auto_attribs=True)
class EEIInformationType:
    ExportInformation: Optional[str] = None
    License: Optional[LicenseType] = JStruct[LicenseType]
    DDTCInformation: Optional[DDTCInformationType] = JStruct[DDTCInformationType]


@s(auto_attribs=True)
class ExcludeFromFormType:
    FormType: Optional[str] = None


@s(auto_attribs=True)
class PackageAssociatedType:
    PackageNumber: Optional[str] = None
    ProductAmount: Optional[str] = None
    ProductNotes: Optional[str] = None


@s(auto_attribs=True)
class PackingListInfoType:
    PackageAssociated: Optional[PackageAssociatedType] = JStruct[PackageAssociatedType]


@s(auto_attribs=True)
class ScheduleBType:
    Number: Optional[str] = None
    Quantity: Optional[str] = None
    UnitOfMeasurement: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]


@s(auto_attribs=True)
class UnitType:
    Number: Optional[str] = None
    Value: Optional[str] = None
    UnitOfMeasurement: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]


@s(auto_attribs=True)
class ProductType:
    Description: Optional[str] = None
    Unit: Optional[UnitType] = JStruct[UnitType]
    CommodityCode: Optional[str] = None
    PartNumber: Optional[str] = None
    OriginCountryCode: Optional[str] = None
    JointProductionIndicator: Optional[str] = None
    NetCostCode: Optional[str] = None
    NetCostDateRange: Optional[BlanketPeriodType] = JStruct[BlanketPeriodType]
    PreferenceCriteria: Optional[str] = None
    ProducerInfo: Optional[str] = None
    MarksAndNumbers: Optional[str] = None
    NumberOfPackagesPerCommodity: Optional[str] = None
    ProductWeight: Optional[WeightType] = JStruct[WeightType]
    VehicleID: Optional[str] = None
    ScheduleB: Optional[ScheduleBType] = JStruct[ScheduleBType]
    ExportType: Optional[str] = None
    SEDTotalValue: Optional[str] = None
    ExcludeFromForm: Optional[ExcludeFromFormType] = JStruct[ExcludeFromFormType]
    PackingListInfo: Optional[PackingListInfoType] = JStruct[PackingListInfoType]
    EEIInformation: Optional[EEIInformationType] = JStruct[EEIInformationType]


@s(auto_attribs=True)
class LanguageForUPSPremiumCareType:
    Language: Optional[str] = None


@s(auto_attribs=True)
class UPSPremiumCareFormType:
    ShipmentDate: Optional[str] = None
    PageSize: Optional[str] = None
    PrintType: Optional[str] = None
    NumOfCopies: Optional[str] = None
    LanguageForUPSPremiumCare: Optional[LanguageForUPSPremiumCareType] = JStruct[LanguageForUPSPremiumCareType]


@s(auto_attribs=True)
class UserCreatedFormType:
    DocumentID: Optional[str] = None


@s(auto_attribs=True)
class InternationalFormsType:
    FormType: Optional[str] = None
    UserCreatedForm: List[UserCreatedFormType] = JList[UserCreatedFormType]
    UPSPremiumCareForm: Optional[UPSPremiumCareFormType] = JStruct[UPSPremiumCareFormType]
    CN22Form: Optional[CN22FormType] = JStruct[CN22FormType]
    AdditionalDocumentIndicator: Optional[str] = None
    FormGroupIdName: Optional[str] = None
    EEIFilingOption: Optional[EEIFilingOptionType] = JStruct[EEIFilingOptionType]
    Contacts: Optional[ContactsType] = JStruct[ContactsType]
    Product: List[ProductType] = JList[ProductType]
    InvoiceNumber: Optional[str] = None
    InvoiceDate: Optional[str] = None
    PurchaseOrderNumber: Optional[str] = None
    TermsOfShipment: Optional[str] = None
    ReasonForExport: Optional[str] = None
    Comments: Optional[str] = None
    DeclarationStatement: Optional[str] = None
    Discount: Optional[DiscountType] = JStruct[DiscountType]
    FreightCharges: Optional[DiscountType] = JStruct[DiscountType]
    InsuranceCharges: Optional[DiscountType] = JStruct[DiscountType]
    OtherCharges: Optional[OtherChargesType] = JStruct[OtherChargesType]
    CurrencyCode: Optional[str] = None
    BlanketPeriod: Optional[BlanketPeriodType] = JStruct[BlanketPeriodType]
    ExportDate: Optional[str] = None
    ExportingCarrier: Optional[str] = None
    CarrierID: Optional[str] = None
    InBondCode: Optional[str] = None
    EntryNumber: Optional[str] = None
    PointOfOrigin: Optional[str] = None
    PointOfOriginType: Optional[str] = None
    ModeOfTransport: Optional[str] = None
    PortOfExport: Optional[str] = None
    PortOfUnloading: Optional[str] = None
    LoadingPier: Optional[str] = None
    PartiesToTransaction: Optional[str] = None
    RoutedExportTransactionIndicator: Optional[str] = None
    ContainerizedIndicator: Optional[str] = None
    OverridePaperlessIndicator: Optional[str] = None
    ShipperMemo: Optional[str] = None
    HazardousMaterialsIndicator: Optional[str] = None


@s(auto_attribs=True)
class LabelDeliveryType:
    EMail: Optional[MailType] = JStruct[MailType]
    LabelLinksIndicator: Optional[str] = None


@s(auto_attribs=True)
class LocaleType:
    Language: Optional[str] = None
    Dialect: Optional[str] = None


@s(auto_attribs=True)
class MessageType:
    PhoneNumber: Optional[str] = None


@s(auto_attribs=True)
class NotificationElementType:
    NotificationCode: Optional[int] = None
    EMail: Optional[MailType] = JStruct[MailType]
    VoiceMessage: Optional[MessageType] = JStruct[MessageType]
    TextMessage: Optional[MessageType] = JStruct[MessageType]
    Locale: Optional[LocaleType] = JStruct[LocaleType]


@s(auto_attribs=True)
class EMailMessageType:
    EMailAddress: Optional[str] = None
    UndeliverableEMailAddress: Optional[str] = None


@s(auto_attribs=True)
class PreAlertNotificationType:
    EMailMessage: Optional[EMailMessageType] = JStruct[EMailMessageType]
    VoiceMessage: Optional[MessageType] = JStruct[MessageType]
    TextMessage: Optional[MessageType] = JStruct[MessageType]
    Locale: Optional[LocaleType] = JStruct[LocaleType]


@s(auto_attribs=True)
class RestrictedArticlesType:
    AlcoholicBeveragesIndicator: Optional[str] = None
    DiagnosticSpecimensIndicator: Optional[str] = None
    PerishablesIndicator: Optional[str] = None
    PlantsIndicator: Optional[str] = None
    SeedsIndicator: Optional[str] = None
    SpecialExceptionsIndicator: Optional[str] = None
    TobaccoIndicator: Optional[str] = None


@s(auto_attribs=True)
class ShipmentServiceOptionsType:
    SaturdayPickupIndicator: Optional[str] = None
    SaturdayDeliveryIndicator: Optional[str] = None
    COD: Optional[CodType] = JStruct[CodType]
    AccessPointCOD: Optional[InvoiceLineTotalType] = JStruct[InvoiceLineTotalType]
    DeliverToAddresseeOnlyIndicator: Optional[str] = None
    DirectDeliveryOnlyIndicator: Optional[str] = None
    Notification: List[NotificationElementType] = JList[NotificationElementType]
    LabelDelivery: Optional[LabelDeliveryType] = JStruct[LabelDeliveryType]
    InternationalForms: Optional[InternationalFormsType] = JStruct[InternationalFormsType]
    DeliveryConfirmation: Optional[ShipmentServiceOptionsDeliveryConfirmationType] = JStruct[ShipmentServiceOptionsDeliveryConfirmationType]
    ReturnOfDocumentIndicator: Optional[str] = None
    ImportControlIndicator: Optional[str] = None
    LabelMethod: Optional[LabelImageFormatType] = JStruct[LabelImageFormatType]
    CommercialInvoiceRemovalIndicator: Optional[str] = None
    UPScarbonneutralIndicator: Optional[str] = None
    PreAlertNotification: List[PreAlertNotificationType] = JList[PreAlertNotificationType]
    ExchangeForwardIndicator: Optional[str] = None
    HoldForPickupIndicator: Optional[str] = None
    DropoffAtUPSFacilityIndicator: Optional[str] = None
    LiftGateForPickupIndicator: Optional[str] = None
    LiftGateForDeliveryIndicator: Optional[str] = None
    SDLShipmentIndicator: Optional[str] = None
    EPRAReleaseCode: Optional[str] = None
    RestrictedArticles: Optional[RestrictedArticlesType] = JStruct[RestrictedArticlesType]
    InsideDelivery: Optional[str] = None
    ItemDisposal: Optional[str] = None


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
    Package: List[PackageType] = JList[PackageType]


@s(auto_attribs=True)
class ShipmentRequestType:
    Request: Optional[RequestType] = JStruct[RequestType]
    Shipment: Optional[ShipmentType] = JStruct[ShipmentType]
    LabelSpecification: Optional[LabelSpecificationType] = JStruct[LabelSpecificationType]
    ReceiptSpecification: Optional[ReceiptSpecificationType] = JStruct[ReceiptSpecificationType]


@s(auto_attribs=True)
class ShippingRequestType:
    ShipmentRequest: Optional[ShipmentRequestType] = JStruct[ShipmentRequestType]
