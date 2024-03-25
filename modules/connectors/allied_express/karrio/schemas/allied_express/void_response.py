from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class Ns1CancelDispatchJobResponseType:
    xmlnsns1: Optional[str] = None
    result: Optional[int] = None


@s(auto_attribs=True)
class SoapenvBodyType:
    ns1cancelDispatchJobResponse: Optional[Ns1CancelDispatchJobResponseType] = JStruct[Ns1CancelDispatchJobResponseType]


@s(auto_attribs=True)
class SoapenvEnvelopeType:
    xmlnssoapenv: Optional[str] = None
    xmlnsxsd: Optional[str] = None
    xmlnsxsi: Optional[str] = None
    soapenvBody: Optional[SoapenvBodyType] = JStruct[SoapenvBodyType]


@s(auto_attribs=True)
class VoidResponseType:
    soapenvEnvelope: Optional[SoapenvEnvelopeType] = JStruct[SoapenvEnvelopeType]
