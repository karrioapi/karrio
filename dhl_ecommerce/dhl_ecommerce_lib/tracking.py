import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Package:
    consignmentNoteNumber: Optional[int] = None
    productId: Optional[int] = None
    originalOrderedProductName: Optional[str] = None
    customerConfirmationNumber: Optional[int] = None
    deliveryConfirmationFlag: Optional[int] = None
    intelligentMailBarcodeFlag: Optional[int] = None
    weight: Optional[int] = None


@attr.s(auto_attribs=True)
class Pickup:
    pickup: Optional[str] = None
    customerName: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[int] = None


@attr.s(auto_attribs=True)
class Recipient:
    postalCode: Optional[int] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


@attr.s(auto_attribs=True)
class DetailedMailItemData:
    recipient: Optional[Recipient] = JStruct[Recipient]
    pickup: Optional[Pickup] = None
    package: Optional[Package] = None


@attr.s(auto_attribs=True)
class DetailedMailItem:
    url: Optional[str] = None
    totalcount: Optional[int] = None
    data: Optional[DetailedMailItemData] = JStruct[DetailedMailItemData]


@attr.s(auto_attribs=True)
class Errors:
    code: Optional[str] = None
    message: Optional[str] = None


@attr.s(auto_attribs=True)
class Meta:
    timestamp: Optional[str] = None
    code: Optional[int] = None


@attr.s(auto_attribs=True)
class Error:
    meta: Optional[Meta] = JStruct[Meta]
    errors: Optional[Errors] = JStruct[Errors]


@attr.s(auto_attribs=True)
class Events:
    id: Optional[int] = None
    description: Optional[str] = None


@attr.s(auto_attribs=True)
class MailItemPackage:
    customerConfirmationNumber: Optional[int] = None
    mailIdentifier: Optional[str] = None
    dspNumber: Optional[int] = None


@attr.s(auto_attribs=True)
class MailItemData:
    recipient: Optional[Recipient] = JStruct[Recipient]
    package: Optional[MailItemPackage] = JStruct[MailItemPackage]
    events: Optional[Events] = JStruct[Events]


@attr.s(auto_attribs=True)
class MailItem:
    url: Optional[str] = None
    totalcount: Optional[int] = None
    data: Optional[MailItemData] = JStruct[MailItemData]
