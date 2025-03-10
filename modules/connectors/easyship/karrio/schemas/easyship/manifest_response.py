import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DocumentType:
    format: typing.Optional[str] = None
    url: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ManifestType:
    courier_account_id: typing.Optional[str] = None
    courier_umbrella_name: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    document: typing.Optional[DocumentType] = jstruct.JStruct[DocumentType]
    id: typing.Optional[str] = None
    ref_number: typing.Optional[str] = None
    shipments_count: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class MetaType:
    request_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ManifestResponseType:
    manifest: typing.Optional[ManifestType] = jstruct.JStruct[ManifestType]
    meta: typing.Optional[MetaType] = jstruct.JStruct[MetaType]
