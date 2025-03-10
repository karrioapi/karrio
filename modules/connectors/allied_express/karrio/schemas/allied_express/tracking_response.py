import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class StatusBarcodesListType:
    consignmentNote: typing.Optional[str] = None
    depotLocation: typing.Optional[str] = None
    scannedBarcode: typing.Optional[str] = None
    scannedStatus: typing.Optional[str] = None
    scannnedTimestamp: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResultType:
    statusBarcodesList: typing.Optional[StatusBarcodesListType] = jstruct.JStruct[StatusBarcodesListType]


@attr.s(auto_attribs=True)
class Ns1GetShipmentsStatusResponseType:
    xmlnsns1: typing.Optional[str] = None
    result: typing.Optional[ResultType] = jstruct.JStruct[ResultType]


@attr.s(auto_attribs=True)
class SoapenvBodyType:
    ns1getShipmentsStatusResponse: typing.Optional[Ns1GetShipmentsStatusResponseType] = jstruct.JStruct[Ns1GetShipmentsStatusResponseType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    soapenvBody: typing.Optional[SoapenvBodyType] = jstruct.JStruct[SoapenvBodyType]
