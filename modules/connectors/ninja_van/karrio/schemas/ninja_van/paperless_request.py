from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class MetaType:
    shipDocumentType: Optional[str] = None
    formCode: Optional[str] = None
    trackingNumber: Optional[str] = None
    shipmentDate: Optional[str] = None
    originLocationCode: Optional[str] = None
    originCountryCode: Optional[str] = None
    destinationLocationCode: Optional[str] = None
    destinationCountryCode: Optional[str] = None


@s(auto_attribs=True)
class DocumentType:
    workflowName: Optional[str] = None
    carrierCode: Optional[str] = None
    name: Optional[str] = None
    contentType: Optional[str] = None
    meta: Optional[MetaType] = JStruct[MetaType]


@s(auto_attribs=True)
class PaperlessRequestType:
    document: Optional[DocumentType] = JStruct[DocumentType]
    attachment: Optional[str] = None
