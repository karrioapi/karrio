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
class SoapenvEnvelopeSoapenvBodyType:
    ns1calculatePriceResponse: Optional[Ns1CalculatePriceResponseType] = JStruct[Ns1CalculatePriceResponseType]


@s(auto_attribs=True)
class SoapenvEnvelopeType:
    xmlnssoapenv: Optional[str] = None
    xmlnsxsd: Optional[str] = None
    xmlnsxsi: Optional[str] = None
    soapenvBody: Optional[SoapenvEnvelopeSoapenvBodyType] = JStruct[SoapenvEnvelopeSoapenvBodyType]


@s(auto_attribs=True)
class PriceType:
    soapenvEnvelope: Optional[SoapenvEnvelopeType] = JStruct[SoapenvEnvelopeType]


@s(auto_attribs=True)
class Ns1GetLabelResponseType:
    xmlnsns1: Optional[str] = None
    result: Optional[str] = None


@s(auto_attribs=True)
class LabelResponseSoapenvBodyType:
    ns1getLabelResponse: Optional[Ns1GetLabelResponseType] = JStruct[Ns1GetLabelResponseType]


@s(auto_attribs=True)
class LabelResponseType:
    Price: Optional[PriceType] = JStruct[PriceType]
    Tracking: Optional[str] = None
    soapenvBody: Optional[LabelResponseSoapenvBodyType] = JStruct[LabelResponseSoapenvBodyType]
