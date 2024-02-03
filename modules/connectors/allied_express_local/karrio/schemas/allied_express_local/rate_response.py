from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class SurchargeType:
    chargeCode: Optional[str] = None
    description: Optional[str] = None
    netValue: Optional[str] = None
    quantity: Optional[int] = None


@s(auto_attribs=True)
class ResultType:
    jobCharge: Optional[str] = None
    surcharges: List[SurchargeType] = JList[SurchargeType]
    totalCharge: Optional[str] = None


@s(auto_attribs=True)
class Ns1CalculatePriceResponseType:
    xmlnsns1: Optional[str] = None
    result: Optional[ResultType] = JStruct[ResultType]


@s(auto_attribs=True)
class SoapenvBodyType:
    ns1calculatePriceResponse: Optional[Ns1CalculatePriceResponseType] = JStruct[Ns1CalculatePriceResponseType]


@s(auto_attribs=True)
class SoapenvEnvelopeType:
    xmlnssoapenv: Optional[str] = None
    xmlnsxsd: Optional[str] = None
    xmlnsxsi: Optional[str] = None
    soapenvBody: Optional[SoapenvBodyType] = JStruct[SoapenvBodyType]


@s(auto_attribs=True)
class RateResponseType:
    soapenvEnvelope: Optional[SoapenvEnvelopeType] = JStruct[SoapenvEnvelopeType]
