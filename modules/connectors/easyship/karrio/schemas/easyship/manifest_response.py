from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class DocumentType:
    format: Optional[str] = None
    url: Optional[str] = None


@s(auto_attribs=True)
class ManifestType:
    courier_account_id: Optional[str] = None
    courier_umbrella_name: Optional[str] = None
    created_at: Optional[str] = None
    document: Optional[DocumentType] = JStruct[DocumentType]
    id: Optional[str] = None
    ref_number: Optional[str] = None
    shipments_count: Optional[int] = None


@s(auto_attribs=True)
class MetaType:
    request_id: Optional[str] = None


@s(auto_attribs=True)
class ManifestResponseType:
    manifest: Optional[ManifestType] = JStruct[ManifestType]
    meta: Optional[MetaType] = JStruct[MetaType]
