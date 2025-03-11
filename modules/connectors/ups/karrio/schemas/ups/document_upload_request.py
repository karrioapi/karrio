import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TransactionReferenceType:
    CustomerContext: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RequestType:
    TransactionReference: typing.Optional[TransactionReferenceType] = jstruct.JStruct[TransactionReferenceType]


@attr.s(auto_attribs=True)
class UserCreatedFormType:
    UserCreatedFormFileName: typing.Optional[str] = None
    UserCreatedFormFileFormat: typing.Optional[str] = None
    UserCreatedFormDocumentType: typing.Optional[str] = None
    UserCreatedFormFile: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UploadRequestType:
    Request: typing.Optional[RequestType] = jstruct.JStruct[RequestType]
    ShipperNumber: typing.Optional[str] = None
    UserCreatedForm: typing.Optional[typing.List[UserCreatedFormType]] = jstruct.JList[UserCreatedFormType]


@attr.s(auto_attribs=True)
class DocumentUploadRequestType:
    UploadRequest: typing.Optional[UploadRequestType] = jstruct.JStruct[UploadRequestType]
