from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class FormsHistoryDocumentIDType:
    DocumentID: Optional[str] = None


@s(auto_attribs=True)
class ResponseStatusType:
    Code: Optional[int] = None
    Description: Optional[str] = None


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    ResponseStatus: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
    TransactionReference: Optional[TransactionReferenceType] = JStruct[
        TransactionReferenceType
    ]


@s(auto_attribs=True)
class UploadResponseType:
    Response: Optional[ResponseType] = JStruct[ResponseType]
    FormsHistoryDocumentID: Optional[FormsHistoryDocumentIDType] = JStruct[
        FormsHistoryDocumentIDType
    ]


@s(auto_attribs=True)
class DocumentUploadResponseType:
    UploadResponse: Optional[UploadResponseType] = JStruct[UploadResponseType]
