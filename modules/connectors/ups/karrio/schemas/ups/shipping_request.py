import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelImageFormatType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelStockSizeType:
    Height: typing.Optional[str] = None
    Width: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelSpecificationType:
    LabelImageFormat: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    HTTPUserAgent: typing.Optional[str] = None
    LabelStockSize: typing.Optional[LabelStockSizeType] = jstruct.JStruct[LabelStockSizeType]
    Instruction: typing.Optional[typing.List[LabelImageFormatType]] = jstruct.JList[LabelImageFormatType]
    CharacterSet: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiptSpecificationType:
    ImageFormat: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestType:
    SubVersion: typing.Optional[int] = None
    RequestOption: typing.Optional[str] = None
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class AlternateDeliveryAddressAddressType:
    AddressLine: typing.Optional[str] = None
    City: typing.Optional[str] = None
    StateProvinceCode: typing.Optional[str] = None
    PostalCode: typing.Optional[str] = None
    CountryCode: typing.Optional[str] = None
    ResidentialAddressIndicator: typing.Optional[str] = None
    Town: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AlternateDeliveryAddressType:
    Name: typing.Optional[str] = None
    AttentionName: typing.Optional[str] = None
    UPSAccessPointID: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]


@attr.s(auto_attribs=True)
class DGSignatoryInfoType:
    Name: typing.Optional[str] = None
    Title: typing.Optional[str] = None
    Place: typing.Optional[str] = None
    Date: typing.Optional[str] = None
    ShipperDeclaration: typing.Optional[str] = None
    UploadOnlyIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FRSPaymentInformationAddressType:
    PostalCode: typing.Optional[int] = None
    CountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FRSPaymentInformationType:
    Type: typing.Optional[str] = None
    AccountNumber: typing.Optional[str] = None
    Address: typing.Optional[FRSPaymentInformationAddressType] = jstruct.JStruct[FRSPaymentInformationAddressType]


@attr.s(auto_attribs=True)
class AdjustedHeightType:
    Value: typing.Optional[int] = None
    UnitOfMeasurement: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]


@attr.s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    Length: typing.Optional[int] = None
    Width: typing.Optional[int] = None
    Height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class HandlingUnitsType:
    Quantity: typing.Optional[int] = None
    Type: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
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
    UnitOfMeasurement: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    Weight: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HazMatPackageInformationType:
    AllPackedInOneIndicator: typing.Optional[str] = None
    OverPackedIndicator: typing.Optional[str] = None
    QValue: typing.Optional[str] = None
    OuterPackagingType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CodType:
    CODFundsCode: typing.Optional[int] = None
    CODAmount: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]


@attr.s(auto_attribs=True)
class PackageServiceOptionsDeliveryConfirmationType:
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
class MailType:
    EMailAddress: typing.Optional[str] = None
    UndeliverableEMailAddress: typing.Optional[str] = None
    FromEMailAddress: typing.Optional[str] = None
    FromName: typing.Optional[str] = None
    Memo: typing.Optional[str] = None
    Subject: typing.Optional[str] = None
    SubjectCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageServiceOptionsNotificationType:
    NotificationCode: typing.Optional[int] = None
    Email: typing.Optional[MailType] = jstruct.JStruct[MailType]


@attr.s(auto_attribs=True)
class PackageServiceOptionsType:
    DeliveryConfirmation: typing.Optional[PackageServiceOptionsDeliveryConfirmationType] = jstruct.JStruct[PackageServiceOptionsDeliveryConfirmationType]
    DeclaredValue: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    COD: typing.Optional[CodType] = jstruct.JStruct[CodType]
    AccessPointCOD: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    ShipperReleaseIndicator: typing.Optional[str] = None
    Notification: typing.Optional[PackageServiceOptionsNotificationType] = jstruct.JStruct[PackageServiceOptionsNotificationType]
    HazMat: typing.Optional[HazMatType] = jstruct.JStruct[HazMatType]
    DryIce: typing.Optional[DryIceType] = jstruct.JStruct[DryIceType]
    UPSPremiumCareIndicator: typing.Optional[str] = None
    ProactiveIndicator: typing.Optional[str] = None
    PackageIdentifier: typing.Optional[str] = None
    ClinicalTrialsID: typing.Optional[str] = None
    RefrigerationIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReferenceNumberType:
    BarCodeIndicator: typing.Optional[str] = None
    Code: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HandlingInstructionsType:
    Instruction: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UPSPremierType:
    Category: typing.Optional[str] = None
    SensorID: typing.Optional[str] = None
    HandlingInstructions: typing.Optional[HandlingInstructionsType] = jstruct.JStruct[HandlingInstructionsType]


@attr.s(auto_attribs=True)
class PackageType:
    Description: typing.Optional[str] = None
    PalletDescription: typing.Optional[str] = None
    NumOfPieces: typing.Optional[int] = None
    UnitPrice: typing.Optional[str] = None
    Packaging: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    DimWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    PackageWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    LargePackageIndicator: typing.Optional[str] = None
    ReferenceNumber: typing.Optional[ReferenceNumberType] = jstruct.JStruct[ReferenceNumberType]
    AdditionalHandlingIndicator: typing.Optional[str] = None
    UPSPremier: typing.Optional[UPSPremierType] = jstruct.JStruct[UPSPremierType]
    PackageServiceOptions: typing.Optional[PackageServiceOptionsType] = jstruct.JStruct[PackageServiceOptionsType]
    Commodity: typing.Optional[CommodityType] = jstruct.JStruct[CommodityType]
    HazMatPackageInformation: typing.Optional[HazMatPackageInformationType] = jstruct.JStruct[HazMatPackageInformationType]


@attr.s(auto_attribs=True)
class BillReceiverAddressType:
    PostalCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BillReceiverType:
    AccountNumber: typing.Optional[str] = None
    Address: typing.Optional[BillReceiverAddressType] = jstruct.JStruct[BillReceiverAddressType]


@attr.s(auto_attribs=True)
class CreditCardType:
    Type: typing.Optional[str] = None
    Number: typing.Optional[str] = None
    ExpirationDate: typing.Optional[int] = None
    SecurityCode: typing.Optional[int] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]


@attr.s(auto_attribs=True)
class BillShipperType:
    AccountNumber: typing.Optional[str] = None
    CreditCard: typing.Optional[CreditCardType] = jstruct.JStruct[CreditCardType]
    AlternatePaymentMethod: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BillThirdPartyType:
    AccountNumber: typing.Optional[str] = None
    CertifiedElectronicMail: typing.Optional[str] = None
    InterchangeSystemCode: typing.Optional[str] = None
    Address: typing.Optional[FRSPaymentInformationAddressType] = jstruct.JStruct[FRSPaymentInformationAddressType]


@attr.s(auto_attribs=True)
class ShipmentChargeType:
    Type: typing.Optional[str] = None
    BillShipper: typing.Optional[BillShipperType] = jstruct.JStruct[BillShipperType]
    BillReceiver: typing.Optional[BillReceiverType] = jstruct.JStruct[BillReceiverType]
    BillThirdParty: typing.Optional[BillThirdPartyType] = jstruct.JStruct[BillThirdPartyType]
    ConsigneeBilledIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PaymentInformationType:
    ShipmentCharge: typing.Optional[typing.List[ShipmentChargeType]] = jstruct.JList[ShipmentChargeType]
    SplitDutyVATIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PromotionalDiscountInformationType:
    PromoCode: typing.Optional[str] = None
    PromoAliasCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipFromPhoneType:
    Number: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class VendorInfoType:
    VendorCollectIDTypeCode: typing.Optional[str] = None
    VendorCollectIDNumber: typing.Optional[int] = None
    ConsigneeType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipFromType:
    Name: typing.Optional[str] = None
    AttentionName: typing.Optional[str] = None
    CompanyDisplayableName: typing.Optional[str] = None
    TaxIdentificationNumber: typing.Optional[int] = None
    TaxId: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    Phone: typing.Optional[ShipFromPhoneType] = jstruct.JStruct[ShipFromPhoneType]
    FaxNumber: typing.Optional[int] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]
    VendorInfo: typing.Optional[VendorInfoType] = jstruct.JStruct[VendorInfoType]


@attr.s(auto_attribs=True)
class ShipToPhoneType:
    Number: typing.Optional[str] = None
    Extension: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipToType:
    Name: typing.Optional[str] = None
    AttentionName: typing.Optional[str] = None
    CompanyDisplayableName: typing.Optional[str] = None
    TaxIdentificationNumber: typing.Optional[int] = None
    Phone: typing.Optional[ShipToPhoneType] = jstruct.JStruct[ShipToPhoneType]
    FaxNumber: typing.Optional[int] = None
    EMailAddress: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]
    LocationID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentRatingOptionsType:
    NegotiatedRatesIndicator: typing.Optional[str] = None
    FRSShipmentIndicator: typing.Optional[str] = None
    RateChartIndicator: typing.Optional[str] = None
    UserLevelDiscountIndicator: typing.Optional[str] = None
    TPFCNegotiatedRatesIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentServiceOptionsDeliveryConfirmationType:
    DCISType: typing.Optional[int] = None
    DCISNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BlanketPeriodType:
    BeginDate: typing.Optional[str] = None
    EndDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CN22ContentType:
    CN22ContentQuantity: typing.Optional[str] = None
    CN22ContentDescription: typing.Optional[str] = None
    CN22ContentWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    CN22ContentTotalValue: typing.Optional[str] = None
    CN22ContentCurrencyCode: typing.Optional[str] = None
    CN22ContentCountryOfOrigin: typing.Optional[str] = None
    CN22ContentTariffNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CN22FormType:
    LabelSize: typing.Optional[str] = None
    PrintsPerPage: typing.Optional[str] = None
    LabelPrintType: typing.Optional[str] = None
    CN22Type: typing.Optional[str] = None
    CN22OtherDescription: typing.Optional[str] = None
    FoldHereText: typing.Optional[str] = None
    CN22Content: typing.Optional[CN22ContentType] = jstruct.JStruct[CN22ContentType]


@attr.s(auto_attribs=True)
class ForwardAgentType:
    CompanyName: typing.Optional[str] = None
    TaxIdentificationNumber: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]


@attr.s(auto_attribs=True)
class IntermediateConsigneeType:
    CompanyName: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]


@attr.s(auto_attribs=True)
class ProducerType:
    Option: typing.Optional[str] = None
    CompanyName: typing.Optional[str] = None
    TaxIdentificationNumber: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]
    AttentionName: typing.Optional[str] = None
    Phone: typing.Optional[ShipToPhoneType] = jstruct.JStruct[ShipToPhoneType]
    EMailAddress: typing.Optional[str] = None
    Name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UltimateConsigneeType:
    CompanyName: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]
    UltimateConsigneeType: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]


@attr.s(auto_attribs=True)
class ContactsType:
    ForwardAgent: typing.Optional[ForwardAgentType] = jstruct.JStruct[ForwardAgentType]
    UltimateConsignee: typing.Optional[UltimateConsigneeType] = jstruct.JStruct[UltimateConsigneeType]
    IntermediateConsignee: typing.Optional[IntermediateConsigneeType] = jstruct.JStruct[IntermediateConsigneeType]
    Producer: typing.Optional[ProducerType] = jstruct.JStruct[ProducerType]
    SoldTo: typing.Optional[ProducerType] = jstruct.JStruct[ProducerType]


@attr.s(auto_attribs=True)
class DiscountType:
    MonetaryValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipperFiledType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    PreDepartureITNNumber: typing.Optional[str] = None
    ExemptionLegend: typing.Optional[str] = None
    EEIShipmentReferenceNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UPSFiledType:
    POA: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]


@attr.s(auto_attribs=True)
class EEIFilingOptionType:
    Code: typing.Optional[str] = None
    EMailAddress: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    UPSFiled: typing.Optional[UPSFiledType] = jstruct.JStruct[UPSFiledType]
    ShipperFiled: typing.Optional[ShipperFiledType] = jstruct.JStruct[ShipperFiledType]


@attr.s(auto_attribs=True)
class OtherChargesType:
    MonetaryValue: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DDTCInformationType:
    ITARExemptionNumber: typing.Optional[str] = None
    USMLCategoryCode: typing.Optional[str] = None
    EligiblePartyIndicator: typing.Optional[str] = None
    RegistrationNumber: typing.Optional[str] = None
    Quantity: typing.Optional[str] = None
    UnitOfMeasurement: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    SignificantMilitaryEquipmentIndicator: typing.Optional[str] = None
    ACMNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LicenseType:
    Number: typing.Optional[str] = None
    Code: typing.Optional[str] = None
    LicenseLineValue: typing.Optional[str] = None
    ECCNNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EEIInformationType:
    ExportInformation: typing.Optional[str] = None
    License: typing.Optional[LicenseType] = jstruct.JStruct[LicenseType]
    DDTCInformation: typing.Optional[DDTCInformationType] = jstruct.JStruct[DDTCInformationType]


@attr.s(auto_attribs=True)
class ExcludeFromFormType:
    FormType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageAssociatedType:
    PackageNumber: typing.Optional[str] = None
    ProductAmount: typing.Optional[str] = None
    ProductNotes: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackingListInfoType:
    PackageAssociated: typing.Optional[PackageAssociatedType] = jstruct.JStruct[PackageAssociatedType]


@attr.s(auto_attribs=True)
class ScheduleBType:
    Number: typing.Optional[str] = None
    Quantity: typing.Optional[str] = None
    UnitOfMeasurement: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]


@attr.s(auto_attribs=True)
class UnitType:
    Number: typing.Optional[str] = None
    Value: typing.Optional[str] = None
    UnitOfMeasurement: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]


@attr.s(auto_attribs=True)
class ProductType:
    Description: typing.Optional[str] = None
    Unit: typing.Optional[UnitType] = jstruct.JStruct[UnitType]
    CommodityCode: typing.Optional[str] = None
    PartNumber: typing.Optional[str] = None
    OriginCountryCode: typing.Optional[str] = None
    JointProductionIndicator: typing.Optional[str] = None
    NetCostCode: typing.Optional[str] = None
    NetCostDateRange: typing.Optional[BlanketPeriodType] = jstruct.JStruct[BlanketPeriodType]
    PreferenceCriteria: typing.Optional[str] = None
    ProducerInfo: typing.Optional[str] = None
    MarksAndNumbers: typing.Optional[str] = None
    NumberOfPackagesPerCommodity: typing.Optional[str] = None
    ProductWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    VehicleID: typing.Optional[str] = None
    ScheduleB: typing.Optional[ScheduleBType] = jstruct.JStruct[ScheduleBType]
    ExportType: typing.Optional[str] = None
    SEDTotalValue: typing.Optional[str] = None
    ExcludeFromForm: typing.Optional[ExcludeFromFormType] = jstruct.JStruct[ExcludeFromFormType]
    PackingListInfo: typing.Optional[PackingListInfoType] = jstruct.JStruct[PackingListInfoType]
    EEIInformation: typing.Optional[EEIInformationType] = jstruct.JStruct[EEIInformationType]


@attr.s(auto_attribs=True)
class LanguageForUPSPremiumCareType:
    Language: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UPSPremiumCareFormType:
    ShipmentDate: typing.Optional[str] = None
    PageSize: typing.Optional[str] = None
    PrintType: typing.Optional[str] = None
    NumOfCopies: typing.Optional[str] = None
    LanguageForUPSPremiumCare: typing.Optional[LanguageForUPSPremiumCareType] = jstruct.JStruct[LanguageForUPSPremiumCareType]


@attr.s(auto_attribs=True)
class UserCreatedFormType:
    DocumentID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalFormsType:
    FormType: typing.Optional[str] = None
    UserCreatedForm: typing.Optional[typing.List[UserCreatedFormType]] = jstruct.JList[UserCreatedFormType]
    UPSPremiumCareForm: typing.Optional[UPSPremiumCareFormType] = jstruct.JStruct[UPSPremiumCareFormType]
    CN22Form: typing.Optional[CN22FormType] = jstruct.JStruct[CN22FormType]
    AdditionalDocumentIndicator: typing.Optional[str] = None
    FormGroupIdName: typing.Optional[str] = None
    EEIFilingOption: typing.Optional[EEIFilingOptionType] = jstruct.JStruct[EEIFilingOptionType]
    Contacts: typing.Optional[ContactsType] = jstruct.JStruct[ContactsType]
    Product: typing.Optional[typing.List[ProductType]] = jstruct.JList[ProductType]
    InvoiceNumber: typing.Optional[str] = None
    InvoiceDate: typing.Optional[str] = None
    PurchaseOrderNumber: typing.Optional[str] = None
    TermsOfShipment: typing.Optional[str] = None
    ReasonForExport: typing.Optional[str] = None
    Comments: typing.Optional[str] = None
    DeclarationStatement: typing.Optional[str] = None
    Discount: typing.Optional[DiscountType] = jstruct.JStruct[DiscountType]
    FreightCharges: typing.Optional[DiscountType] = jstruct.JStruct[DiscountType]
    InsuranceCharges: typing.Optional[DiscountType] = jstruct.JStruct[DiscountType]
    OtherCharges: typing.Optional[OtherChargesType] = jstruct.JStruct[OtherChargesType]
    CurrencyCode: typing.Optional[str] = None
    BlanketPeriod: typing.Optional[BlanketPeriodType] = jstruct.JStruct[BlanketPeriodType]
    ExportDate: typing.Optional[str] = None
    ExportingCarrier: typing.Optional[str] = None
    CarrierID: typing.Optional[str] = None
    InBondCode: typing.Optional[str] = None
    EntryNumber: typing.Optional[str] = None
    PointOfOrigin: typing.Optional[str] = None
    PointOfOriginType: typing.Optional[str] = None
    ModeOfTransport: typing.Optional[str] = None
    PortOfExport: typing.Optional[str] = None
    PortOfUnloading: typing.Optional[str] = None
    LoadingPier: typing.Optional[str] = None
    PartiesToTransaction: typing.Optional[str] = None
    RoutedExportTransactionIndicator: typing.Optional[str] = None
    ContainerizedIndicator: typing.Optional[str] = None
    OverridePaperlessIndicator: typing.Optional[str] = None
    ShipperMemo: typing.Optional[str] = None
    HazardousMaterialsIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelDeliveryType:
    EMail: typing.Optional[MailType] = jstruct.JStruct[MailType]
    LabelLinksIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LocaleType:
    Language: typing.Optional[str] = None
    Dialect: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MessageType:
    PhoneNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NotificationElementType:
    NotificationCode: typing.Optional[int] = None
    EMail: typing.Optional[MailType] = jstruct.JStruct[MailType]
    VoiceMessage: typing.Optional[MessageType] = jstruct.JStruct[MessageType]
    TextMessage: typing.Optional[MessageType] = jstruct.JStruct[MessageType]
    Locale: typing.Optional[LocaleType] = jstruct.JStruct[LocaleType]


@attr.s(auto_attribs=True)
class EMailMessageType:
    EMailAddress: typing.Optional[str] = None
    UndeliverableEMailAddress: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PreAlertNotificationType:
    EMailMessage: typing.Optional[EMailMessageType] = jstruct.JStruct[EMailMessageType]
    VoiceMessage: typing.Optional[MessageType] = jstruct.JStruct[MessageType]
    TextMessage: typing.Optional[MessageType] = jstruct.JStruct[MessageType]
    Locale: typing.Optional[LocaleType] = jstruct.JStruct[LocaleType]


@attr.s(auto_attribs=True)
class RestrictedArticlesType:
    AlcoholicBeveragesIndicator: typing.Optional[str] = None
    DiagnosticSpecimensIndicator: typing.Optional[str] = None
    PerishablesIndicator: typing.Optional[str] = None
    PlantsIndicator: typing.Optional[str] = None
    SeedsIndicator: typing.Optional[str] = None
    SpecialExceptionsIndicator: typing.Optional[str] = None
    TobaccoIndicator: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipmentServiceOptionsType:
    SaturdayPickupIndicator: typing.Optional[str] = None
    SaturdayDeliveryIndicator: typing.Optional[str] = None
    COD: typing.Optional[CodType] = jstruct.JStruct[CodType]
    AccessPointCOD: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    DeliverToAddresseeOnlyIndicator: typing.Optional[str] = None
    DirectDeliveryOnlyIndicator: typing.Optional[str] = None
    Notification: typing.Optional[typing.List[NotificationElementType]] = jstruct.JList[NotificationElementType]
    LabelDelivery: typing.Optional[LabelDeliveryType] = jstruct.JStruct[LabelDeliveryType]
    InternationalForms: typing.Optional[InternationalFormsType] = jstruct.JStruct[InternationalFormsType]
    DeliveryConfirmation: typing.Optional[ShipmentServiceOptionsDeliveryConfirmationType] = jstruct.JStruct[ShipmentServiceOptionsDeliveryConfirmationType]
    ReturnOfDocumentIndicator: typing.Optional[str] = None
    ImportControlIndicator: typing.Optional[str] = None
    LabelMethod: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    CommercialInvoiceRemovalIndicator: typing.Optional[str] = None
    UPScarbonneutralIndicator: typing.Optional[str] = None
    PreAlertNotification: typing.Optional[typing.List[PreAlertNotificationType]] = jstruct.JList[PreAlertNotificationType]
    ExchangeForwardIndicator: typing.Optional[str] = None
    HoldForPickupIndicator: typing.Optional[str] = None
    DropoffAtUPSFacilityIndicator: typing.Optional[str] = None
    LiftGateForPickupIndicator: typing.Optional[str] = None
    LiftGateForDeliveryIndicator: typing.Optional[str] = None
    SDLShipmentIndicator: typing.Optional[str] = None
    EPRAReleaseCode: typing.Optional[str] = None
    RestrictedArticles: typing.Optional[RestrictedArticlesType] = jstruct.JStruct[RestrictedArticlesType]
    InsideDelivery: typing.Optional[str] = None
    ItemDisposal: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShipperType:
    Name: typing.Optional[str] = None
    AttentionName: typing.Optional[str] = None
    CompanyDisplayableName: typing.Optional[str] = None
    TaxIdentificationNumber: typing.Optional[int] = None
    Phone: typing.Optional[ShipToPhoneType] = jstruct.JStruct[ShipToPhoneType]
    ShipperNumber: typing.Optional[str] = None
    FaxNumber: typing.Optional[str] = None
    EMailAddress: typing.Optional[str] = None
    Address: typing.Optional[AlternateDeliveryAddressAddressType] = jstruct.JStruct[AlternateDeliveryAddressAddressType]


@attr.s(auto_attribs=True)
class ShipmentType:
    Description: typing.Optional[str] = None
    ReturnService: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    DocumentsOnlyIndicator: typing.Optional[str] = None
    Shipper: typing.Optional[ShipperType] = jstruct.JStruct[ShipperType]
    ShipTo: typing.Optional[ShipToType] = jstruct.JStruct[ShipToType]
    AlternateDeliveryAddress: typing.Optional[AlternateDeliveryAddressType] = jstruct.JStruct[AlternateDeliveryAddressType]
    ShipFrom: typing.Optional[ShipFromType] = jstruct.JStruct[ShipFromType]
    PaymentInformation: typing.Optional[PaymentInformationType] = jstruct.JStruct[PaymentInformationType]
    FRSPaymentInformation: typing.Optional[FRSPaymentInformationType] = jstruct.JStruct[FRSPaymentInformationType]
    FreightShipmentInformation: typing.Optional[FreightShipmentInformationType] = jstruct.JStruct[FreightShipmentInformationType]
    GoodsNotInFreeCirculationIndicator: typing.Optional[str] = None
    PromotionalDiscountInformation: typing.Optional[PromotionalDiscountInformationType] = jstruct.JStruct[PromotionalDiscountInformationType]
    DGSignatoryInfo: typing.Optional[DGSignatoryInfoType] = jstruct.JStruct[DGSignatoryInfoType]
    ShipmentRatingOptions: typing.Optional[ShipmentRatingOptionsType] = jstruct.JStruct[ShipmentRatingOptionsType]
    MovementReferenceNumber: typing.Optional[str] = None
    ReferenceNumber: typing.Optional[ReferenceNumberType] = jstruct.JStruct[ReferenceNumberType]
    Service: typing.Optional[LabelImageFormatType] = jstruct.JStruct[LabelImageFormatType]
    InvoiceLineTotal: typing.Optional[InvoiceLineTotalType] = jstruct.JStruct[InvoiceLineTotalType]
    NumOfPiecesInShipment: typing.Optional[int] = None
    USPSEndorsement: typing.Optional[str] = None
    MILabelCN22Indicator: typing.Optional[str] = None
    SubClassification: typing.Optional[str] = None
    CostCenter: typing.Optional[str] = None
    CostCenterBarcodeIndicator: typing.Optional[str] = None
    PackageID: typing.Optional[str] = None
    PackageIDBarcodeIndicator: typing.Optional[str] = None
    IrregularIndicator: typing.Optional[str] = None
    ShipmentIndicationType: typing.Optional[typing.List[LabelImageFormatType]] = jstruct.JList[LabelImageFormatType]
    MIDualReturnShipmentKey: typing.Optional[str] = None
    RatingMethodRequestedIndicator: typing.Optional[str] = None
    TaxInformationIndicator: typing.Optional[str] = None
    ShipmentServiceOptions: typing.Optional[ShipmentServiceOptionsType] = jstruct.JStruct[ShipmentServiceOptionsType]
    Locale: typing.Optional[str] = None
    ShipmentValueThresholdCode: typing.Optional[str] = None
    MasterCartonID: typing.Optional[str] = None
    MasterCartonIndicator: typing.Optional[str] = None
    BarCodeImageIndicator: typing.Optional[str] = None
    BarCodeAndLabelIndicator: typing.Optional[str] = None
    ShipmentDate: typing.Optional[int] = None
    Package: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    Request: typing.Optional[RequestType] = jstruct.JStruct[RequestType]
    Shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
    LabelSpecification: typing.Optional[LabelSpecificationType] = jstruct.JStruct[LabelSpecificationType]
    ReceiptSpecification: typing.Optional[ReceiptSpecificationType] = jstruct.JStruct[ReceiptSpecificationType]


@attr.s(auto_attribs=True)
class ShippingRequestType:
    ShipmentRequest: typing.Optional[ShipmentRequestType] = jstruct.JStruct[ShipmentRequestType]
