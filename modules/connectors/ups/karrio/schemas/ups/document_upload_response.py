import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class FormsHistoryDocumentIDType:
    DocumentID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseStatusType:
    Code: typing.Optional[int] = None
    Description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ResponseType:
    ResponseStatus: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
    Alert: typing.Optional[typing.List[ResponseStatusType]] = jstruct.JList[ResponseStatusType]
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class UploadResponseType:
    Response: typing.Optional[ResponseType] = jstruct.JStruct[ResponseType]
    FormsHistoryDocumentID: typing.Optional[typing.List[FormsHistoryDocumentIDType]] = jstruct.JList[FormsHistoryDocumentIDType]


@attr.s(auto_attribs=True)
class DocumentUploadResponseType:
    UploadResponse: typing.Optional[UploadResponseType] = jstruct.JStruct[UploadResponseType]
