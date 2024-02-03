from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class StatusBarcodesListType:
    consignmentNote: Optional[str] = None
    depotLocation: Optional[str] = None
    scannedBarcode: Optional[str] = None
    scannedStatus: Optional[str] = None
    scannnedTimestamp: Optional[str] = None


@s(auto_attribs=True)
class ResultType:
    statusBarcodesList: Optional[StatusBarcodesListType] = JStruct[StatusBarcodesListType]


@s(auto_attribs=True)
class Ns1GetShipmentsStatusResponseType:
    xmlnsns1: Optional[str] = None
    result: Optional[ResultType] = JStruct[ResultType]


@s(auto_attribs=True)
class SoapenvBodyType:
    ns1getShipmentsStatusResponse: Optional[Ns1GetShipmentsStatusResponseType] = JStruct[Ns1GetShipmentsStatusResponseType]


@s(auto_attribs=True)
class TrackingResponseType:
    soapenvBody: Optional[SoapenvBodyType] = JStruct[SoapenvBodyType]
