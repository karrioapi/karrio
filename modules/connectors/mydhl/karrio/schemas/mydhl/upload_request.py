import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class DocumentImageType:
    typeCode: typing.Optional[str] = None
    imageFormat: typing.Optional[str] = None
    content: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UploadRequestType:
    originalPlannedShippingDate: typing.Optional[str] = None
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    productCode: typing.Optional[str] = None
    documentImages: typing.Optional[typing.List[DocumentImageType]] = jstruct.JList[DocumentImageType]
