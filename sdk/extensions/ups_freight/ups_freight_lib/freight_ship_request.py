from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class MiscellaneousType:
    WSVersion: Optional[str] = None
    ReleaseID: Optional[str] = None


@s(auto_attribs=True)
class DeclaredValueType:
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class ServiceType:
    Code: Optional[str] = None


@s(auto_attribs=True)
class CommodityDimensionsType:
    UnitOfMeasurement: Optional[ServiceType] = JStruct[ServiceType]
    Length: Optional[str] = None
    Width: Optional[str] = None
    Height: Optional[str] = None


@s(auto_attribs=True)
class NMFCCommodityType:
    PrimeCode: Optional[str] = None
    SubCode: Optional[str] = None


@s(auto_attribs=True)
class WeightType:
    UnitOfMeasurement: Optional[ServiceType] = JStruct[ServiceType]
    Value: Optional[str] = None


@s(auto_attribs=True)
class CommodityType:
    CommodityID: Optional[str] = None
    Description: Optional[str] = None
    Weight: Optional[WeightType] = JStruct[WeightType]
    Dimensions: Optional[CommodityDimensionsType] = JStruct[CommodityDimensionsType]
    NumberOfPieces: Optional[int] = None
    PackagingType: Optional[ServiceType] = JStruct[ServiceType]
    DangerousGoodsIndicator: Optional[str] = None
    CommodityValue: Optional[DeclaredValueType] = JStruct[DeclaredValueType]
    FreightClass: Optional[int] = None
    NMFCCommodityCode: Optional[str] = None
    NMFCCommodity: Optional[NMFCCommodityType] = JStruct[NMFCCommodityType]


@s(auto_attribs=True)
class PrintSizeType:
    Length: Optional[str] = None
    Width: Optional[str] = None


@s(auto_attribs=True)
class ImageType:
    Type: Optional[ServiceType] = JStruct[ServiceType]
    LabelsPerPage: Optional[str] = None
    Format: Optional[ServiceType] = JStruct[ServiceType]
    PrintFormat: Optional[ServiceType] = JStruct[ServiceType]
    PrintSize: Optional[PrintSizeType] = JStruct[PrintSizeType]


@s(auto_attribs=True)
class DocumentsType:
    Image: List[ImageType] = JList[ImageType]


@s(auto_attribs=True)
class ConfirmationNumberType:
    Type: Optional[ServiceType] = JStruct[ServiceType]
    Value: Optional[str] = None


@s(auto_attribs=True)
class ExistingShipmentIDType:
    ShipmentNumber: Optional[str] = None
    BOLID: Optional[str] = None
    ConfirmationNumber: Optional[ConfirmationNumberType] = JStruct[ConfirmationNumberType]


@s(auto_attribs=True)
class HandlingUnitType:
    Quantity: Optional[int] = None
    Type: Optional[ServiceType] = JStruct[ServiceType]


@s(auto_attribs=True)
class HandlingUnitElementType:
    Quantity: Optional[str] = None
    Type: Optional[ServiceType] = JStruct[ServiceType]
    Dimensions: Optional[CommodityDimensionsType] = JStruct[CommodityDimensionsType]


@s(auto_attribs=True)
class AddressType:
    AddressLine: Optional[str] = None
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    Town: Optional[str] = None
    PostalCode: Optional[str] = None
    CountryCode: Optional[str] = None


@s(auto_attribs=True)
class PhoneType:
    Number: Optional[str] = None
    Extension: Optional[str] = None


@s(auto_attribs=True)
class ShipFromType:
    Name: Optional[str] = None
    Address: Optional[AddressType] = JStruct[AddressType]
    ShipperNumber: Optional[str] = None
    AttentionName: Optional[str] = None
    Phone: Optional[PhoneType] = JStruct[PhoneType]
    FaxNumber: Optional[str] = None
    TaxIdentificationNumber: Optional[str] = None
    EMailAddress: Optional[str] = None


@s(auto_attribs=True)
class PaymentInformationType:
    Payer: Optional[ShipFromType] = JStruct[ShipFromType]
    ShipmentBillingOption: Optional[ServiceType] = JStruct[ServiceType]


@s(auto_attribs=True)
class EMailNotificationType:
    EMailAddress: Optional[str] = None
    EventType: Optional[str] = None
    FailedEMail: Optional[str] = None


@s(auto_attribs=True)
class PickupNotificationsType:
    EMailNotification: Optional[EMailNotificationType] = JStruct[EMailNotificationType]


@s(auto_attribs=True)
class PomType:
    POMNumber: Optional[str] = None
    POMNumberType: Optional[str] = None
    PickupNotifications: Optional[PickupNotificationsType] = JStruct[PickupNotificationsType]


@s(auto_attribs=True)
class RequesterType:
    ThirdPartyIndicator: Optional[str] = None
    AttentionName: Optional[str] = None
    EMailAddress: Optional[str] = None
    Name: Optional[str] = None
    Phone: Optional[PhoneType] = JStruct[PhoneType]


@s(auto_attribs=True)
class PickupRequestType:
    AdditionalComments: Optional[str] = None
    Requester: Optional[RequesterType] = JStruct[RequesterType]
    PickupDate: Optional[int] = None
    EarliestTimeReady: Optional[str] = None
    LatestTimeReady: Optional[int] = None
    POM: Optional[PomType] = JStruct[PomType]


@s(auto_attribs=True)
class NumberType:
    Code: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class ReferenceType:
    Number: Optional[NumberType] = JStruct[NumberType]
    BarCodeIndicator: Optional[str] = None
    NumberOfCartons: Optional[str] = None
    Weight: Optional[WeightType] = JStruct[WeightType]


@s(auto_attribs=True)
class CodType:
    CODValue: Optional[DeclaredValueType] = JStruct[DeclaredValueType]
    CODPaymentMethod: Optional[ServiceType] = JStruct[ServiceType]
    CODBillingOption: Optional[ServiceType] = JStruct[ServiceType]
    RemitTo: Optional[ShipFromType] = JStruct[ShipFromType]


@s(auto_attribs=True)
class DangerousGoodsType:
    Name: Optional[str] = None
    Phone: Optional[PhoneType] = JStruct[PhoneType]
    TransportationMode: Optional[ServiceType] = JStruct[ServiceType]


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
class EmailType:
    EMailAddress: Optional[str] = None
    EMailText: Optional[str] = None
    UndeliverableEMailAddress: Optional[str] = None
    Subject: Optional[str] = None


@s(auto_attribs=True)
class EMailInformationType:
    EMailType: Optional[ServiceType] = JStruct[ServiceType]
    Email: Optional[EmailType] = JStruct[EmailType]


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
    UnitOfMeasurement: Optional[ServiceType] = JStruct[ServiceType]
    Value: Optional[ValueType] = JStruct[ValueType]


@s(auto_attribs=True)
class OverSeasLegType:
    Dimensions: Optional[OverSeasLegDimensionsType] = JStruct[OverSeasLegDimensionsType]


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
    EMailInformation: Optional[EMailInformationType] = JStruct[EMailInformationType]
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


@s(auto_attribs=True)
class ShipmentType:
    ShipFrom: Optional[ShipFromType] = JStruct[ShipFromType]
    ShipperNumber: Optional[int] = None
    ShipTo: Optional[ShipFromType] = JStruct[ShipFromType]
    PaymentInformation: Optional[PaymentInformationType] = JStruct[PaymentInformationType]
    Service: Optional[ServiceType] = JStruct[ServiceType]
    HandlingUnitOne: Optional[HandlingUnitType] = JStruct[HandlingUnitType]
    HandlingUnitTwo: Optional[HandlingUnitType] = JStruct[HandlingUnitType]
    ExistingShipmentID: Optional[ExistingShipmentIDType] = JStruct[ExistingShipmentIDType]
    HandlingInstructions: Optional[str] = None
    DeliveryInstructions: Optional[str] = None
    PickupInstructions: Optional[str] = None
    Commodity: List[CommodityType] = JList[CommodityType]
    Reference: Optional[ReferenceType] = JStruct[ReferenceType]
    ShipmentServiceOptions: Optional[ShipmentServiceOptionsType] = JStruct[ShipmentServiceOptionsType]
    PickupRequest: Optional[PickupRequestType] = JStruct[PickupRequestType]
    Documents: Optional[DocumentsType] = JStruct[DocumentsType]
    TimeInTransitIndicator: Optional[str] = None
    HandlingUnits: List[HandlingUnitElementType] = JList[HandlingUnitElementType]
    DensityEligibleIndicator: Optional[str] = None


@s(auto_attribs=True)
class FreightShipRequestClassType:
    Shipment: Optional[ShipmentType] = JStruct[ShipmentType]
    Miscellaneous: Optional[MiscellaneousType] = JStruct[MiscellaneousType]


@s(auto_attribs=True)
class FreightShipRequestType:
    FreightShipRequest: Optional[FreightShipRequestClassType] = JStruct[FreightShipRequestClassType]
