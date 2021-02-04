from pydantic.dataclasses import dataclass
from typing import Optional, List


@dataclass
class Package:
    consignmentNoteNumber: Optional[int] = None
    productId: Optional[int] = None
    originalOrderedProductName: Optional[str] = None
    customerConfirmationNumber: Optional[int] = None
    deliveryConfirmationFlag: Optional[int] = None
    intelligentMailBarcodeFlag: Optional[int] = None
    weight: Optional[int] = None


@dataclass
class Pickup:
    pickup: Optional[str] = None
    customerName: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[int] = None


@dataclass
class Recipient:
    postalCode: Optional[int] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


@dataclass
class DetailedMailItemData:
    recipient: Optional[Recipient] = None
    pickup: Optional[Pickup] = None
    package: Optional[Package] = None


@dataclass
class DetailedMailItem:
    url: Optional[str] = None
    totalcount: Optional[int] = None
    data: Optional[DetailedMailItemData] = None


@dataclass
class Errors:
    code: Optional[str] = None
    message: Optional[str] = None


@dataclass
class Meta:
    timestamp: Optional[str] = None
    code: Optional[int] = None


@dataclass
class Error:
    meta: Optional[Meta] = None
    errors: Optional[Errors] = None


@dataclass
class Events:
    id: Optional[int] = None
    description: Optional[str] = None


@dataclass
class MailItemPackage:
    customerConfirmationNumber: Optional[int] = None
    mailIdentifier: Optional[str] = None
    dspNumber: Optional[int] = None


@dataclass
class MailItemData:
    recipient: Optional[Recipient] = None
    package: Optional[MailItemPackage] = None
    events: Optional[Events] = None


@dataclass
class MailItem:
    url: Optional[str] = None
    totalcount: Optional[int] = None
    data: Optional[MailItemData] = None
