import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class SurchargeType:
    chargeCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    netValue: typing.Optional[str] = None
    quantity: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ResultType:
    jobCharge: typing.Optional[str] = None
    surcharges: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    totalCharge: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Ns1CalculatePriceResponseType:
    xmlnsns1: typing.Optional[str] = None
    result: typing.Optional[ResultType] = jstruct.JStruct[ResultType]


@attr.s(auto_attribs=True)
class SoapenvEnvelopeSoapenvBodyType:
    ns1calculatePriceResponse: typing.Optional[Ns1CalculatePriceResponseType] = jstruct.JStruct[Ns1CalculatePriceResponseType]


@attr.s(auto_attribs=True)
class SoapenvEnvelopeType:
    xmlnssoapenv: typing.Optional[str] = None
    xmlnsxsd: typing.Optional[str] = None
    xmlnsxsi: typing.Optional[str] = None
    soapenvBody: typing.Optional[SoapenvEnvelopeSoapenvBodyType] = jstruct.JStruct[SoapenvEnvelopeSoapenvBodyType]


@attr.s(auto_attribs=True)
class PriceType:
    soapenvEnvelope: typing.Optional[SoapenvEnvelopeType] = jstruct.JStruct[SoapenvEnvelopeType]


@attr.s(auto_attribs=True)
class Ns1GetLabelResponseType:
    xmlnsns1: typing.Optional[str] = None
    result: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LabelResponseSoapenvBodyType:
    ns1getLabelResponse: typing.Optional[Ns1GetLabelResponseType] = jstruct.JStruct[Ns1GetLabelResponseType]


@attr.s(auto_attribs=True)
class LabelResponseType:
    Price: typing.Optional[PriceType] = jstruct.JStruct[PriceType]
    Tracking: typing.Optional[str] = None
    soapenvBody: typing.Optional[LabelResponseSoapenvBodyType] = jstruct.JStruct[LabelResponseSoapenvBodyType]
