from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: Optional[str] = None


@s(auto_attribs=True)
class RequestType:
    TransactionReference: Optional[TransactionReferenceType] = JStruct[TransactionReferenceType]


@s(auto_attribs=True)
class UserCreatedFormType:
    UserCreatedFormFileName: Optional[str] = None
    UserCreatedFormFileFormat: Optional[str] = None
    UserCreatedFormDocumentType: Optional[str] = None
    UserCreatedFormFile: Optional[str] = None


@s(auto_attribs=True)
class UploadRequestType:
    Request: Optional[RequestType] = JStruct[RequestType]
    ShipperNumber: Optional[str] = None
    UserCreatedForm: List[UserCreatedFormType] = JList[UserCreatedFormType]


@s(auto_attribs=True)
class DocumentUploadRequestType:
    UploadRequest: Optional[UploadRequestType] = JStruct[UploadRequestType]
