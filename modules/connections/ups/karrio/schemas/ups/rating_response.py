from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class BaseServiceChargeType:
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class AlertType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class BillingWeightType:
    UnitOfMeasurement: Optional[AlertType] = JStruct[AlertType]
    Weight: Optional[str] = None


@s(auto_attribs=True)
class FreightDensityRateType:
    Density: Optional[str] = None
    TotalCubicFeet: Optional[str] = None


@s(auto_attribs=True)
class AdjustedHeightType:
    Value: Optional[str] = None
    UnitOfMeasurement: Optional[AlertType] = JStruct[AlertType]


@s(auto_attribs=True)
class DimensionsType:
    UnitOfMeasurement: Optional[AlertType] = JStruct[AlertType]
    Length: Optional[str] = None
    Width: Optional[str] = None
    Height: Optional[str] = None


@s(auto_attribs=True)
class HandlingUnitsType:
    Quantity: Optional[str] = None
    Type: Optional[AlertType] = JStruct[AlertType]
    Dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    AdjustedHeight: Optional[AdjustedHeightType] = JStruct[AdjustedHeightType]


@s(auto_attribs=True)
class TransportationChargesType:
    GrossCharge: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    DiscountAmount: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    DiscountPercentage: Optional[str] = None
    NetCharge: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]


@s(auto_attribs=True)
class FRSShipmentDataType:
    TransportationCharges: Optional[TransportationChargesType] = JStruct[TransportationChargesType]
    FreightDensityRate: Optional[FreightDensityRateType] = JStruct[FreightDensityRateType]
    HandlingUnits: Optional[HandlingUnitsType] = JStruct[HandlingUnitsType]


@s(auto_attribs=True)
class GuaranteedDeliveryType:
    BusinessDaysInTransit: Optional[int] = None
    DeliveryByTime: Optional[str] = None


@s(auto_attribs=True)
class ItemizedChargeType:
    Code: Optional[str] = None
    Description: Optional[str] = None
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[str] = None
    SubType: Optional[str] = None


@s(auto_attribs=True)
class TaxChargeType:
    Type: Optional[str] = None
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class NegotiatedRateChargesType:
    ItemizedCharges: List[ItemizedChargeType] = JList[ItemizedChargeType]
    TaxCharges: List[TaxChargeType] = JList[TaxChargeType]
    TotalCharge: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    TotalChargesWithTaxes: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]


@s(auto_attribs=True)
class NegotiatedChargesType:
    ItemizedCharges: List[ItemizedChargeType] = JList[ItemizedChargeType]


@s(auto_attribs=True)
class RateModifierType:
    ModifierType: Optional[str] = None
    ModifierDesc: Optional[str] = None
    CurrencyCode: Optional[str] = None
    Amount: Optional[str] = None


@s(auto_attribs=True)
class RatedPackageType:
    BaseServiceCharge: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    TransportationCharges: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    ServiceOptionsCharges: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    TotalCharges: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    Weight: Optional[str] = None
    BillingWeight: Optional[BillingWeightType] = JStruct[BillingWeightType]
    Accessorial: List[AlertType] = JList[AlertType]
    ItemizedCharges: List[ItemizedChargeType] = JList[ItemizedChargeType]
    NegotiatedCharges: Optional[NegotiatedChargesType] = JStruct[NegotiatedChargesType]
    RateModifier: Optional[RateModifierType] = JStruct[RateModifierType]


@s(auto_attribs=True)
class ArrivalType:
    Date: Optional[str] = None
    Time: Optional[str] = None


@s(auto_attribs=True)
class EstimatedArrivalType:
    Arrival: Optional[ArrivalType] = JStruct[ArrivalType]
    BusinessDaysInTransit: Optional[str] = None
    Pickup: Optional[ArrivalType] = JStruct[ArrivalType]
    DayOfWeek: Optional[str] = None
    CustomerCenterCutoff: Optional[str] = None
    DelayCount: Optional[str] = None
    HolidayCount: Optional[str] = None
    RestDays: Optional[str] = None
    TotalTransitDays: Optional[str] = None


@s(auto_attribs=True)
class ServiceType:
    Description: Optional[str] = None


@s(auto_attribs=True)
class ServiceSummaryType:
    Service: Optional[ServiceType] = JStruct[ServiceType]
    GuaranteedIndicator: Optional[str] = None
    Disclaimer: Optional[str] = None
    EstimatedArrival: Optional[EstimatedArrivalType] = JStruct[EstimatedArrivalType]
    SaturdayDelivery: Optional[str] = None
    SaturdayDeliveryDisclaimer: Optional[str] = None
    SundayDelivery: Optional[str] = None
    SundayDeliveryDisclaimer: Optional[str] = None


@s(auto_attribs=True)
class TimeInTransitType:
    PickupDate: Optional[str] = None
    DocumentsOnlyIndicator: Optional[str] = None
    PackageBillType: Optional[str] = None
    ServiceSummary: Optional[ServiceSummaryType] = JStruct[ServiceSummaryType]
    AutoDutyCode: Optional[str] = None
    Disclaimer: Optional[str] = None


@s(auto_attribs=True)
class RatedShipmentType:
    Disclaimer: List[AlertType] = JList[AlertType]
    Service: Optional[AlertType] = JStruct[AlertType]
    RateChart: Optional[str] = None
    RatedShipmentAlert: List[AlertType] = JList[AlertType]
    BillableWeightCalculationMethod: Optional[str] = None
    RatingMethod: Optional[str] = None
    BillingWeight: Optional[BillingWeightType] = JStruct[BillingWeightType]
    TransportationCharges: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    BaseServiceCharge: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    ItemizedCharges: List[ItemizedChargeType] = JList[ItemizedChargeType]
    FRSShipmentData: Optional[FRSShipmentDataType] = JStruct[FRSShipmentDataType]
    ServiceOptionsCharges: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    TaxCharges: List[TaxChargeType] = JList[TaxChargeType]
    TotalCharges: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    TotalChargesWithTaxes: Optional[BaseServiceChargeType] = JStruct[BaseServiceChargeType]
    NegotiatedRateCharges: Optional[NegotiatedRateChargesType] = JStruct[NegotiatedRateChargesType]
    RatedPackage: List[RatedPackageType] = JList[RatedPackageType]
    GuaranteedDelivery: Optional[GuaranteedDeliveryType] = JStruct[GuaranteedDeliveryType]
    TimeInTransit: Optional[TimeInTransitType] = JStruct[TimeInTransitType]
    ScheduledDeliveryDate: Optional[str] = None
    RoarRatedIndicator: Optional[str] = None


@s(auto_attribs=True)
class ElementIdentifierType:
    Code: Optional[str] = None
    Value: Optional[str] = None


@s(auto_attribs=True)
class ElementLevelInformationType:
    Level: Optional[str] = None
    ElementIdentifier: List[ElementIdentifierType] = JList[ElementIdentifierType]


@s(auto_attribs=True)
class AlertDetailType:
    Code: Optional[str] = None
    Description: Optional[str] = None
    ElementLevelInformation: Optional[ElementLevelInformationType] = JStruct[ElementLevelInformationType]


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    ResponseStatus: Optional[AlertType] = JStruct[AlertType]
    Alert: Optional[AlertType] = JStruct[AlertType]
    AlertDetail: Optional[AlertDetailType] = JStruct[AlertDetailType]
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class RateResponseType:
    Response: Optional[ResponseType] = JStruct[ResponseType]
    RatedShipment: List[RatedShipmentType] = JList[RatedShipmentType]


@s(auto_attribs=True)
class RatingResponseType:
    RateResponse: Optional[RateResponseType] = JStruct[RateResponseType]
