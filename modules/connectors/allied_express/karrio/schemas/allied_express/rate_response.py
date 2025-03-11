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
class SoapenvBodyType:
    ns1calculatePriceResponse: typing.Optional[Ns1CalculatePriceResponseType] = jstruct.JStruct[Ns1CalculatePriceResponseType]


@attr.s(auto_attribs=True)
class SoapenvEnvelopeType:
    xmlnssoapenv: typing.Optional[str] = None
    xmlnsxsd: typing.Optional[str] = None
    xmlnsxsi: typing.Optional[str] = None
    soapenvBody: typing.Optional[SoapenvBodyType] = jstruct.JStruct[SoapenvBodyType]


@attr.s(auto_attribs=True)
class RateResponseType:
    soapenvEnvelope: typing.Optional[SoapenvEnvelopeType] = jstruct.JStruct[SoapenvEnvelopeType]
