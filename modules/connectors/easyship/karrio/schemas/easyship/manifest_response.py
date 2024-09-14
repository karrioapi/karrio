from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class DocumentType:
    format: Optional[str] = None
    url: Optional[str] = None


@s(auto_attribs=True)
class ManifestType:
    courieraccountid: Optional[str] = None
    courierumbrellaname: Optional[str] = None
    createdat: Optional[str] = None
    document: Optional[DocumentType] = JStruct[DocumentType]
    id: Optional[str] = None
    refnumber: Optional[str] = None
    shipmentscount: Optional[int] = None


@s(auto_attribs=True)
class MetaType:
    requestid: Optional[str] = None


@s(auto_attribs=True)
class ManifestResponseType:
    manifest: Optional[ManifestType] = JStruct[ManifestType]
    meta: Optional[MetaType] = JStruct[MetaType]
