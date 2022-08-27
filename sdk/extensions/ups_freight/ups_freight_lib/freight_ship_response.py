from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ResponseStatusType:
    Code: Optional[str] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None
    TransactionIdentifier: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    ResponseStatus: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
    Alert: List[ResponseStatusType] = JList[ResponseStatusType]
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class BillableShipmentWeightType:
    Value: Optional[str] = None
    UnitOfMeasurement: Optional[ResponseStatusType] = JStruct[ResponseStatusType]


@s(auto_attribs=True)
class FormsType:
    Type: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
    GraphicImage: Optional[str] = None
    Format: Optional[ResponseStatusType] = JStruct[ResponseStatusType]


@s(auto_attribs=True)
class DocumentsType:
    Image: List[FormsType] = JList[FormsType]
    Forms: Optional[FormsType] = JStruct[FormsType]


@s(auto_attribs=True)
class FreightDensityRateType:
    Density: Optional[str] = None
    TotalCubicFeet: Optional[str] = None


@s(auto_attribs=True)
class RateType:
    Type: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
    Factor: Optional[BillableShipmentWeightType] = JStruct[BillableShipmentWeightType]


@s(auto_attribs=True)
class TimeInTransitType:
    DaysInTransit: Optional[str] = None


@s(auto_attribs=True)
class TotalShipmentChargeType:
    CurrencyCode: Optional[str] = None
    MonetaryValue: Optional[str] = None


@s(auto_attribs=True)
class ShipmentResultsType:
    OriginServiceCenterCode: Optional[str] = None
    PickupRequestConfirmationNumber: Optional[str] = None
    DeliveryDate: Optional[str] = None
    ShipmentNumber: Optional[str] = None
    BOLID: Optional[str] = None
    GuaranteedIndicator: Optional[str] = None
    MinimumChargeAppliedIndicator: Optional[str] = None
    Rate: List[RateType] = JList[RateType]
    FreightDensityRate: Optional[FreightDensityRateType] = JStruct[FreightDensityRateType]
    TotalShipmentCharge: Optional[TotalShipmentChargeType] = JStruct[TotalShipmentChargeType]
    BillableShipmentWeight: Optional[BillableShipmentWeightType] = JStruct[BillableShipmentWeightType]
    Service: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
    Documents: Optional[DocumentsType] = JStruct[DocumentsType]
    TimeInTransit: Optional[TimeInTransitType] = JStruct[TimeInTransitType]


@s(auto_attribs=True)
class FreightShipResponseClassType:
    Response: Optional[ResponseType] = JStruct[ResponseType]
    ShipmentResults: Optional[ShipmentResultsType] = JStruct[ShipmentResultsType]


@s(auto_attribs=True)
class FreightShipResponseType:
    FreightShipResponse: Optional[FreightShipResponseClassType] = JStruct[FreightShipResponseClassType]
