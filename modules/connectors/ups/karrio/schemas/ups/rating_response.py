import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BaseServiceChargeType:
    CurrencyCode: typing.Optional[str] = None
    MonetaryValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseStatusType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BillingWeightType:
    UnitOfMeasurement: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
    Weight: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FreightDensityRateType:
    Density: typing.Optional[str] = None
    TotalCubicFeet: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AdjustedHeightType:
    Value: typing.Optional[str] = None
    UnitOfMeasurement: typing.Optional[typing.Union[ResponseStatusType, str]] = None


@attr.s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: typing.Optional[typing.Union[ResponseStatusType, str]] = None
    Length: typing.Optional[str] = None
    Width: typing.Optional[str] = None
    Height: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class HandlingUnitType:
    Quantity: typing.Optional[str] = None
    Type: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
    Dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]
    AdjustedHeight: typing.Optional[AdjustedHeightType] = jstruct.JStruct[AdjustedHeightType]


@attr.s(auto_attribs=True)
class TransportationChargesType:
    GrossCharge: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    DiscountAmount: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    DiscountPercentage: typing.Optional[str] = None
    NetCharge: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]


@attr.s(auto_attribs=True)
class FRSShipmentDataType:
    TransportationCharges: typing.Optional[TransportationChargesType] = jstruct.JStruct[TransportationChargesType]
    FreightDensityRate: typing.Optional[FreightDensityRateType] = jstruct.JStruct[FreightDensityRateType]
    HandlingUnits: typing.Optional[typing.List[HandlingUnitType]] = jstruct.JList[HandlingUnitType]


@attr.s(auto_attribs=True)
class GuaranteedDeliveryType:
    BusinessDaysInTransit: typing.Optional[str] = None
    DeliveryByTime: typing.Optional[str] = None
    ScheduledDeliveryDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ItemizedChargeClassType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    CurrencyCode: typing.Optional[str] = None
    MonetaryValue: typing.Optional[str] = None
    SubType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateModifierType:
    ModifierType: typing.Optional[str] = None
    ModifierDesc: typing.Optional[str] = None
    Amount: typing.Optional[str] = None
    CurrencyCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TaxChargeType:
    Type: typing.Optional[str] = None
    MonetaryValue: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NegotiatedRateChargesType:
    ItemizedCharges: typing.Optional[typing.List[ItemizedChargeClassType]] = jstruct.JList[ItemizedChargeClassType]
    TaxCharges: typing.Optional[typing.List[TaxChargeType]] = jstruct.JList[TaxChargeType]
    TotalCharge: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    TotalChargesWithTaxes: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    BaseServiceCharge: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    RateModifier: typing.Optional[typing.List[RateModifierType]] = jstruct.JList[RateModifierType]


@attr.s(auto_attribs=True)
class NegotiatedChargesType:
    ItemizedCharges: typing.Optional[typing.List[typing.Union[ItemizedChargeClassType, str]]] = None
    BaseServiceCharge: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    TransportationCharges: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    ServiceOptionsCharges: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    TotalCharge: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    RateModifier: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class SimpleRateType:
    Code: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RatedPackageType:
    BaseServiceCharge: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    TransportationCharges: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    ServiceOptionsCharges: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    TotalCharges: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    Weight: typing.Optional[str] = None
    BillingWeight: typing.Optional[BillingWeightType] = jstruct.JStruct[BillingWeightType]
    Accessorial: typing.Optional[typing.List[ResponseStatusType]] = jstruct.JList[ResponseStatusType]
    ItemizedCharges: typing.Optional[typing.List[ItemizedChargeClassType]] = jstruct.JList[ItemizedChargeClassType]
    NegotiatedCharges: typing.Optional[NegotiatedChargesType] = jstruct.JStruct[NegotiatedChargesType]
    RateModifier: typing.Optional[typing.List[RateModifierType]] = jstruct.JList[RateModifierType]
    SimpleRate: typing.Optional[SimpleRateType] = jstruct.JStruct[SimpleRateType]


@attr.s(auto_attribs=True)
class ArrivalType:
    Date: typing.Optional[str] = None
    Time: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class EstimatedArrivalType:
    Arrival: typing.Optional[ArrivalType] = jstruct.JStruct[ArrivalType]
    BusinessDaysInTransit: typing.Optional[str] = None
    Pickup: typing.Optional[ArrivalType] = jstruct.JStruct[ArrivalType]
    DayOfWeek: typing.Optional[str] = None
    CustomerCenterCutoff: typing.Optional[str] = None
    DelayCount: typing.Optional[str] = None
    HolidayCount: typing.Optional[str] = None
    RestDays: typing.Optional[str] = None
    TotalTransitDays: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceType:
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceSummaryType:
    Service: typing.Optional[ServiceType] = jstruct.JStruct[ServiceType]
    GuaranteedIndicator: typing.Optional[str] = None
    Disclaimer: typing.Optional[typing.Union[typing.List[str], str]] = None
    EstimatedArrival: typing.Optional[EstimatedArrivalType] = jstruct.JStruct[EstimatedArrivalType]
    SaturdayDelivery: typing.Optional[str] = None
    SaturdayDeliveryDisclaimer: typing.Optional[str] = None
    SundayDelivery: typing.Optional[str] = None
    SundayDeliveryDisclaimer: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TimeInTransitType:
    PickupDate: typing.Optional[str] = None
    DocumentsOnlyIndicator: typing.Optional[str] = None
    PackageBillType: typing.Optional[str] = None
    ServiceSummary: typing.Optional[ServiceSummaryType] = jstruct.JStruct[ServiceSummaryType]
    AutoDutyCode: typing.Optional[str] = None
    Disclaimer: typing.Optional[typing.Union[typing.List[str], str]] = None


@attr.s(auto_attribs=True)
class RatedShipmentType:
    Disclaimer: typing.Optional[typing.List[ResponseStatusType]] = jstruct.JList[ResponseStatusType]
    Service: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
    RateChart: typing.Optional[str] = None
    RatedShipmentAlert: typing.Optional[typing.List[ResponseStatusType]] = jstruct.JList[ResponseStatusType]
    BillableWeightCalculationMethod: typing.Optional[str] = None
    RatingMethod: typing.Optional[str] = None
    BillingWeight: typing.Optional[BillingWeightType] = jstruct.JStruct[BillingWeightType]
    TransportationCharges: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    BaseServiceCharge: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    ItemizedCharges: typing.Optional[typing.List[ItemizedChargeClassType]] = jstruct.JList[ItemizedChargeClassType]
    FRSShipmentData: typing.Optional[FRSShipmentDataType] = jstruct.JStruct[FRSShipmentDataType]
    ServiceOptionsCharges: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    TaxCharges: typing.Optional[typing.List[TaxChargeType]] = jstruct.JList[TaxChargeType]
    TotalCharges: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    TotalChargesWithTaxes: typing.Optional[BaseServiceChargeType] = jstruct.JStruct[BaseServiceChargeType]
    NegotiatedRateCharges: typing.Optional[NegotiatedRateChargesType] = jstruct.JStruct[NegotiatedRateChargesType]
    RatedPackage: typing.Optional[typing.List[RatedPackageType]] = jstruct.JList[RatedPackageType]
    GuaranteedDelivery: typing.Optional[GuaranteedDeliveryType] = jstruct.JStruct[GuaranteedDeliveryType]
    TimeInTransit: typing.Optional[TimeInTransitType] = jstruct.JStruct[TimeInTransitType]
    ScheduledDeliveryDate: typing.Optional[str] = None
    RoarRatedIndicator: typing.Optional[str] = None
    Zone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ElementIdentifierType:
    Code: typing.Optional[str] = None
    Value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ElementLevelInformationType:
    Level: typing.Optional[str] = None
    ElementIdentifier: typing.Optional[typing.List[ElementIdentifierType]] = jstruct.JList[ElementIdentifierType]


@attr.s(auto_attribs=True)
class AlertDetailType:
    Code: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    ElementLevelInformation: typing.Optional[ElementLevelInformationType] = jstruct.JStruct[ElementLevelInformationType]


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None
    TransactionIdentifier: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseType:
    ResponseStatus: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
    Alert: typing.Optional[typing.List[ResponseStatusType]] = jstruct.JList[ResponseStatusType]
    AlertDetail: typing.Optional[typing.List[AlertDetailType]] = jstruct.JList[AlertDetailType]
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class RateResponseType:
    Response: typing.Optional[ResponseType] = jstruct.JStruct[ResponseType]
    RatedShipment: typing.Optional[typing.List[RatedShipmentType]] = jstruct.JList[RatedShipmentType]


@attr.s(auto_attribs=True)
class RatingResponseType:
    RateResponse: typing.Optional[RateResponseType] = jstruct.JStruct[RateResponseType]
