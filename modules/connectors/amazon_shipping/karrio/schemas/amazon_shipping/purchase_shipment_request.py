import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Size:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestedDocumentSpecification:
    format: typing.Optional[str] = None
    size: typing.Optional[Size] = jstruct.JStruct[Size]
    dpi: typing.Optional[int] = None
    pageLayout: typing.Optional[str] = None
    needFileJoining: typing.Optional[bool] = None
    requestedDocumentTypes: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class PurchaseShipmentRequest:
    requestToken: typing.Optional[str] = None
    rateId: typing.Optional[str] = None
    requestedDocumentSpecification: typing.Optional[RequestedDocumentSpecification] = jstruct.JStruct[RequestedDocumentSpecification]
    requestedValueAddedServices: typing.Any = None
    additionalInputs: typing.Any = None
