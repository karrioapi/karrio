import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetaType:
    shipDocumentType: typing.Optional[str] = None
    formCode: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    shipmentDate: typing.Optional[str] = None
    originLocationCode: typing.Optional[str] = None
    originCountryCode: typing.Optional[str] = None
    destinationLocationCode: typing.Optional[str] = None
    destinationCountryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DocumentType:
    workflowName: typing.Optional[str] = None
    carrierCode: typing.Optional[str] = None
    name: typing.Optional[str] = None
    contentType: typing.Optional[str] = None
    meta: typing.Optional[MetaType] = jstruct.JStruct[MetaType]


@attr.s(auto_attribs=True)
class PaperlessRequestType:
    document: typing.Optional[DocumentType] = jstruct.JStruct[DocumentType]
    attachment: typing.Optional[str] = None
