from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class WarningType:
    warningCode: Optional[str] = None
    warningDescription: Optional[str] = None


@s(auto_attribs=True)
class ExtraServiceType:
    extraService: Optional[int] = None
    name: Optional[str] = None
    priceType: Optional[str] = None
    price: Optional[float] = None
    warnings: List[WarningType] = JList[WarningType]
    SKU: Optional[str] = None


@s(auto_attribs=True)
class FeeType:
    name: Optional[str] = None
    SKU: Optional[str] = None
    price: Optional[float] = None


@s(auto_attribs=True)
class RateType:
    description: Optional[str] = None
    priceType: Optional[str] = None
    price: Optional[float] = None
    weight: Optional[float] = None
    dimWeight: Optional[float] = None
    fees: List[FeeType] = JList[FeeType]
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    mailClass: Optional[str] = None
    zone: Optional[str] = None
    productName: Optional[str] = None
    productDefinition: Optional[str] = None
    processingCategory: Optional[str] = None
    rateIndicator: Optional[str] = None
    destinationEntryFacilityType: Optional[str] = None
    SKU: Optional[str] = None


@s(auto_attribs=True)
class RateOptionType:
    totalBasePrice: Optional[float] = None
    rates: List[RateType] = JList[RateType]
    extraServices: List[ExtraServiceType] = JList[ExtraServiceType]


@s(auto_attribs=True)
class RateResponseType:
    rateOptions: List[RateOptionType] = JList[RateOptionType]
