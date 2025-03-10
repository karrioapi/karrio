import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Ns1CancelDispatchJobResponseType:
    xmlnsns1: typing.Optional[str] = None
    result: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class SoapenvBodyType:
    ns1cancelDispatchJobResponse: typing.Optional[Ns1CancelDispatchJobResponseType] = jstruct.JStruct[Ns1CancelDispatchJobResponseType]


@attr.s(auto_attribs=True)
class SoapenvEnvelopeType:
    xmlnssoapenv: typing.Optional[str] = None
    xmlnsxsd: typing.Optional[str] = None
    xmlnsxsi: typing.Optional[str] = None
    soapenvBody: typing.Optional[SoapenvBodyType] = jstruct.JStruct[SoapenvBodyType]


@attr.s(auto_attribs=True)
class VoidResponseType:
    soapenvEnvelope: typing.Optional[SoapenvEnvelopeType] = jstruct.JStruct[SoapenvEnvelopeType]
