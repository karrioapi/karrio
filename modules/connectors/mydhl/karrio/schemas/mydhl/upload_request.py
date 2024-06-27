from attr import s
from typing import Optional, List
from jstruct import JList


@s(auto_attribs=True)
class AccountType:
    typeCode: Optional[str] = None
    number: Optional[int] = None


@s(auto_attribs=True)
class DocumentImageType:
    typeCode: Optional[str] = None
    imageFormat: Optional[str] = None
    content: Optional[str] = None


@s(auto_attribs=True)
class UploadRequestType:
    originalPlannedShippingDate: Optional[str] = None
    accounts: List[AccountType] = JList[AccountType]
    productCode: Optional[str] = None
    documentImages: List[DocumentImageType] = JList[DocumentImageType]
