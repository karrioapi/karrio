from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class RatingScheduleType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class ServiceType:
    Code: Optional[str] = None


@s(auto_attribs=True)
class BillableShipmentWeightType:
    Value: Optional[str] = None
    UnitOfMeasurement: Optional[ServiceType] = JStruct[ServiceType]


@s(auto_attribs=True)
class RateType:
    Type: Optional[RatingScheduleType] = JStruct[RatingScheduleType]
    Factor: Optional[BillableShipmentWeightType] = JStruct[BillableShipmentWeightType]


@s(auto_attribs=True)
class AlternateRatesResponseType:
    AlternateRateType: Optional[RatingScheduleType] = JStruct[RatingScheduleType]
    Rate: List[RateType] = JList[RateType]
    BillableShipmentWeight: Optional[BillableShipmentWeightType] = JStruct[BillableShipmentWeightType]


@s(auto_attribs=True)
class CommodityType:
    Description: Optional[str] = None
    Weight: Optional[BillableShipmentWeightType] = JStruct[BillableShipmentWeightType]
    AdjustedWeight: Optional[BillableShipmentWeightType] = JStruct[BillableShipmentWeightType]


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None
    TransactionIdentifier: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    ResponseStatus: Optional[RatingScheduleType] = JStruct[RatingScheduleType]
    Alert: List[RatingScheduleType] = JList[RatingScheduleType]
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class TimeInTransitType:
    DaysInTransit: Optional[int] = None


@s(auto_attribs=True)
class TotalShipmentChargeType:
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class FreightRateResponseClassType:
    Response: Optional[ResponseType] = JStruct[ResponseType]
    Rate: List[RateType] = JList[RateType]
    Commodity: Optional[CommodityType] = JStruct[CommodityType]
    TotalShipmentCharge: Optional[TotalShipmentChargeType] = JStruct[TotalShipmentChargeType]
    BillableShipmentWeight: Optional[BillableShipmentWeightType] = JStruct[BillableShipmentWeightType]
    DimensionalWeight: Optional[BillableShipmentWeightType] = JStruct[BillableShipmentWeightType]
    Service: Optional[ServiceType] = JStruct[ServiceType]
    GuaranteedIndicator: Optional[str] = None
    MinimumChargeAppliedIndicator: Optional[str] = None
    AlternateRatesResponse: Optional[AlternateRatesResponseType] = JStruct[AlternateRatesResponseType]
    RatingSchedule: Optional[RatingScheduleType] = JStruct[RatingScheduleType]
    TimeInTransit: Optional[TimeInTransitType] = JStruct[TimeInTransitType]


@s(auto_attribs=True)
class FreightRateResponseType:
    FreightRateResponse: Optional[FreightRateResponseClassType] = JStruct[FreightRateResponseClassType]
