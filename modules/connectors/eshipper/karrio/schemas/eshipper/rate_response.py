from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class SurchargeType:
    name: Optional[str] = None
    amount: Optional[int] = None


@s(auto_attribs=True)
class QuoteType:
    carrierName: Optional[str] = None
    serviceId: Optional[int] = None
    serviceName: Optional[str] = None
    deliveryCarrier: Optional[str] = None
    modeTransport: Optional[str] = None
    transitDays: Optional[str] = None
    baseCharge: Optional[int] = None
    fuelSurcharge: Optional[int] = None
    fuelSurchargePercentage: Optional[int] = None
    carbonNeutralFees: Optional[int] = None
    surcharges: List[SurchargeType] = JList[SurchargeType]
    totalCharge: Optional[int] = None
    processingFees: Optional[int] = None
    taxes: List[SurchargeType] = JList[SurchargeType]
    totalChargedAmount: Optional[int] = None
    currency: Optional[str] = None


@s(auto_attribs=True)
class RateResponseType:
    uuid: Optional[str] = None
    quotes: List[QuoteType] = JList[QuoteType]
    warnings: List[str] = []
    errors: List[str] = []
