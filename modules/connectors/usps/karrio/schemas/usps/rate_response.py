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
    SKU: Optional[str] = None
    priceType: Optional[str] = None
    price: Optional[float] = None
    warnings: List[WarningType] = JList[WarningType]


@s(auto_attribs=True)
class FeeType:
    name: Optional[str] = None
    SKU: Optional[str] = None
    price: Optional[int] = None


@s(auto_attribs=True)
class RateType:
    SKU: Optional[str] = None
    description: Optional[str] = None
    priceType: Optional[str] = None
    price: Optional[float] = None
    weight: Optional[int] = None
    dimWeight: Optional[int] = None
    fees: List[FeeType] = JList[FeeType]
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    mailClass: Optional[str] = None
    zone: Optional[str] = None


@s(auto_attribs=True)
class RateOptionType:
    totalBasePrice: Optional[float] = None
    rates: List[RateType] = JList[RateType]
    extraServices: List[ExtraServiceType] = JList[ExtraServiceType]
    totalPrice: Optional[float] = None


@s(auto_attribs=True)
class RateResponseType:
    rateOptions: List[RateOptionType] = JList[RateOptionType]
