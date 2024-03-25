from attr import s
from typing import Optional, Any
from jstruct import JStruct


@s(auto_attribs=True)
class DiscountClassType:
    xsinil: Optional[int] = None


@s(auto_attribs=True)
class PriceType:
    chargeQuantity: Optional[int] = None
    cubicFactor: Optional[int] = None
    discountClass: Optional[DiscountClassType] = JStruct[DiscountClassType]
    discountRate: Optional[str] = None
    grossPrice: Optional[str] = None
    jobCode: Optional[DiscountClassType] = JStruct[DiscountClassType]
    netPrice: Optional[str] = None
    rateCode: Optional[DiscountClassType] = JStruct[DiscountClassType]
    reason: Any = None


@s(auto_attribs=True)
class PriceDetailType:
    price: Optional[PriceType] = JStruct[PriceType]


@s(auto_attribs=True)
class Ns1GetLabelResponseType:
    xmlnsns1: Optional[str] = None
    result: Any = None


@s(auto_attribs=True)
class SoapenvBodyType:
    ns1getLabelResponse: Optional[Ns1GetLabelResponseType] = JStruct[Ns1GetLabelResponseType]


@s(auto_attribs=True)
class LabelResponseType:
    Tracking: Optional[str] = None
    pricedetail: Optional[PriceDetailType] = JStruct[PriceDetailType]
    result: Optional[str] = None
    soapenvBody: Optional[SoapenvBodyType] = JStruct[SoapenvBodyType]
