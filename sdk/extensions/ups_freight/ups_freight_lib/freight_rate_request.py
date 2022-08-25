from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AccountTypeType:
    Code: Optional[str] = None


@s(auto_attribs=True)
class EightType:
    UnitOfMeasurement: Optional[AccountTypeType] = JStruct[AccountTypeType]
    Value: Optional[str] = None


@s(auto_attribs=True)
class DeclaredValueType:
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class CommodityDimensionsType:
    UnitOfMeasurement: Optional[AccountTypeType] = JStruct[AccountTypeType]
    Length: Optional[str] = None
    Width: Optional[str] = None
    Height: Optional[str] = None


@s(auto_attribs=True)
class NMFCCommodityType:
    PrimeCode: Optional[str] = None
    SubCode: Optional[str] = None


@s(auto_attribs=True)
class CommodityType:
    CommodityID: Optional[str] = None
    Weight: Optional[EightType] = JStruct[EightType]
    AdjustedWeight: Optional[EightType] = JStruct[EightType]
    Dimensions: Optional[CommodityDimensionsType] = JStruct[CommodityDimensionsType]
    NumberOfPieces: Optional[int] = None
    PackagingType: Optional[AccountTypeType] = JStruct[AccountTypeType]
    DangerousGoodsIndicator: Optional[str] = None
    CommodityValue: Optional[DeclaredValueType] = JStruct[DeclaredValueType]
    NMFCCommodityCode: Optional[str] = None
    NMFCCommodity: Optional[NMFCCommodityType] = JStruct[NMFCCommodityType]
    FreightClass: Optional[int] = None


@s(auto_attribs=True)
class OnCallInformationType:
    OnCallPickupIndicator: Optional[str] = None


@s(auto_attribs=True)
class GFPOptionsType:
    GPFAccesorialRateIndicator: Optional[str] = None
    OnCallInformation: Optional[OnCallInformationType] = JStruct[OnCallInformationType]


@s(auto_attribs=True)
class HandlingUnitType:
    Quantity: Optional[int] = None
    Type: Optional[AccountTypeType] = JStruct[AccountTypeType]


@s(auto_attribs=True)
class HandlingUnitElementType:
    Quantity: Optional[str] = None
    Type: Optional[AccountTypeType] = JStruct[AccountTypeType]
    Dimensions: Optional[CommodityDimensionsType] = JStruct[CommodityDimensionsType]


@s(auto_attribs=True)
class AddressType:
    AddressLine: Optional[str] = None
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    Town: Optional[str] = None
    PostalCode: Optional[str] = None
    CountryCode: Optional[str] = None
    ResidentialAddressIndicator: Optional[str] = None


@s(auto_attribs=True)
class ShipToType:
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    ShipperNumber: Optional[str] = None
    AttentionName: Optional[str] = None
    TariffPoint: Optional[str] = None


@s(auto_attribs=True)
class PaymentInformationType:
    Payer: Optional[ShipToType] = JStruct[ShipToType]
    ShipmentBillingOption: Optional[AccountTypeType] = JStruct[AccountTypeType]


@s(auto_attribs=True)
class PickupRequestType:
    PickupDate: Optional[int] = None
    AdditionalComments: Optional[str] = None


@s(auto_attribs=True)
class ShipFromType:
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    TariffPoint: Optional[str] = None
    AttentionName: Optional[str] = None


@s(auto_attribs=True)
class CodType:
    CODValue: Optional[DeclaredValueType] = JStruct[DeclaredValueType]
    CODPaymentMethod: Optional[AccountTypeType] = JStruct[AccountTypeType]
    CODBillingOption: Optional[AccountTypeType] = JStruct[AccountTypeType]
    RemitTo: Optional[ShipToType] = JStruct[ShipToType]


@s(auto_attribs=True)
class PhoneType:
    Number: Optional[str] = None
    Extension: Optional[str] = None


@s(auto_attribs=True)
class DangerousGoodsType:
    Name: Optional[str] = None
    Phone: Optional[PhoneType] = JStruct[PhoneType]
    TransportationMode: Optional[AccountTypeType] = JStruct[AccountTypeType]


@s(auto_attribs=True)
class DeliveryOptionsType:
    CallBeforeDeliveryIndicator: Optional[str] = None
    HolidayDeliveryIndicator: Optional[str] = None
    InsideDeliveryIndicator: Optional[str] = None
    ResidentialDeliveryIndicator: Optional[str] = None
    WeekendDeliveryIndicator: Optional[str] = None
    LiftGateRequiredIndicator: Optional[str] = None
    LimitedAccessDeliveryIndicator: Optional[str] = None


@s(auto_attribs=True)
class HandlingChargeType:
    Percentage: Optional[str] = None
    Amount: Optional[DeclaredValueType] = JStruct[DeclaredValueType]


@s(auto_attribs=True)
class ValueType:
    Cube: Optional[DeclaredValueType] = JStruct[DeclaredValueType]
    CWT: Optional[DeclaredValueType] = JStruct[DeclaredValueType]


@s(auto_attribs=True)
class OverSeasLegDimensionsType:
    Volume: Optional[str] = None
    Height: Optional[str] = None
    Length: Optional[str] = None
    UnitOfMeasurement: Optional[AccountTypeType] = JStruct[AccountTypeType]
    Value: Optional[ValueType] = JStruct[ValueType]


@s(auto_attribs=True)
class OverSeasLegType:
    Dimensions: Optional[OverSeasLegDimensionsType] = JStruct[OverSeasLegDimensionsType]
    Value: Optional[ValueType] = JStruct[ValueType]


@s(auto_attribs=True)
class PickupOptionsType:
    HolidayPickupIndicator: Optional[str] = None
    InsidePickupIndicator: Optional[str] = None
    ResidentialPickupIndicator: Optional[str] = None
    WeekendPickupIndicator: Optional[str] = None
    LiftGateRequiredIndicator: Optional[str] = None
    LimitedAccessPickupIndicator: Optional[str] = None


@s(auto_attribs=True)
class SortingAndSegregatingType:
    Quantity: Optional[str] = None


@s(auto_attribs=True)
class ShipmentServiceOptionsType:
    PickupOptions: Optional[PickupOptionsType] = JStruct[PickupOptionsType]
    DeliveryOptions: Optional[DeliveryOptionsType] = JStruct[DeliveryOptionsType]
    OverSeasLeg: Optional[OverSeasLegType] = JStruct[OverSeasLegType]
    COD: Optional[CodType] = JStruct[CodType]
    DangerousGoods: Optional[DangerousGoodsType] = JStruct[DangerousGoodsType]
    SortingAndSegregating: Optional[SortingAndSegregatingType] = JStruct[SortingAndSegregatingType]
    DeclaredValue: Optional[DeclaredValueType] = JStruct[DeclaredValueType]
    ExcessDeclaredValue: Optional[DeclaredValueType] = JStruct[DeclaredValueType]
    HandlingCharge: Optional[HandlingChargeType] = JStruct[HandlingChargeType]
    FreezableProtectionIndicator: Optional[str] = None
    ExtremeLengthIndicator: Optional[str] = None
    LinearFeet: Optional[str] = None
    AdjustedHeight: Optional[EightType] = JStruct[EightType]


@s(auto_attribs=True)
class FreightRateRequestClassType:
    ShipFrom: Optional[ShipFromType] = JStruct[ShipFromType]
    ShipTo: Optional[ShipToType] = JStruct[ShipToType]
    PaymentInformation: Optional[PaymentInformationType] = JStruct[PaymentInformationType]
    Service: Optional[AccountTypeType] = JStruct[AccountTypeType]
    HandlingUnitOne: Optional[HandlingUnitType] = JStruct[HandlingUnitType]
    HandlingUnitTwo: Optional[HandlingUnitType] = JStruct[HandlingUnitType]
    Commodity: List[CommodityType] = JList[CommodityType]
    ShipmentServiceOptions: Optional[ShipmentServiceOptionsType] = JStruct[ShipmentServiceOptionsType]
    PickupRequest: Optional[PickupRequestType] = JStruct[PickupRequestType]
    AlternateRateOptions: Optional[AccountTypeType] = JStruct[AccountTypeType]
    GFPOptions: Optional[GFPOptionsType] = JStruct[GFPOptionsType]
    AccountType: Optional[AccountTypeType] = JStruct[AccountTypeType]
    ShipmentTotalWeight: Optional[EightType] = JStruct[EightType]
    HandlingUnitWeight: Optional[EightType] = JStruct[EightType]
    AdjustedWeightIndicator: Optional[str] = None
    TimeInTransitIndicator: Optional[str] = None
    HandlingUnits: List[HandlingUnitElementType] = JList[HandlingUnitElementType]
    AdjustedHeightIndicator: Optional[str] = None
    DensityEligibleIndicator: Optional[str] = None
    QuoteNumberIndicator: Optional[str] = None


@s(auto_attribs=True)
class FreightRateRequestType:
    FreightRateRequest: Optional[FreightRateRequestClassType] = JStruct[FreightRateRequestClassType]
