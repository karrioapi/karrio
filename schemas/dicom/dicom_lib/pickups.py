import attr
from jstruct import JStruct, JList, REQUIRED
from typing import Optional, List


@attr.s(auto_attribs=True)
class Contact:
    fullName: str
    extension: Optional[int] = None
    language: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    telephone: Optional[str] = None


@attr.s(auto_attribs=True)
class Shipment:
    id: int
    status: Optional[int] = None


@attr.s(auto_attribs=True)
class Sender:
    city: str
    provinceCode: str
    postalCode: str
    countryCode: str
    customerName: str

    streetNumber: Optional[int] = None
    suite: Optional[int] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    streetType: Optional[str] = None
    streetName: Optional[str] = None
    streetDirection: Optional[str] = None
    customerNickName: Optional[str] = None
    contact: Optional[Contact] = JStruct[Contact]


@attr.s(auto_attribs=True)
class Shipment:
    id: Optional[int] = None
    status: Optional[int] = None


@attr.s(auto_attribs=True)
class Pickup:
    shipments: Optional[List[Shipment]] = JStruct[Shipment]
    id: Optional[int] = None
    officeClose: Optional[str] = None
    date: Optional[str] = None
    ready: Optional[str] = None
    location: Optional[str] = None
    otherLocation: Optional[str] = None
    category: Optional[str] = None
    sender: Optional[Sender] = JStruct[Sender]
    contact: Optional[Contact] = JStruct[Contact]


@attr.s(auto_attribs=True)
class ShipmentPickupRequest:
    date: str
    ready: str
    category: str
    officeClose: str
    contact: Contact = JStruct[Contact, REQUIRED]
    shipments: List[Shipment] = JList[Shipment, REQUIRED]

    location: Optional[str] = None
    otherLocation: Optional[str] = None


@attr.s(auto_attribs=True)
class PickupRequest:
    date: str
    ready: str
    category: str
    officeClose: str
    sender: Sender = JStruct[Sender, REQUIRED]

    location: Optional[str] = None
    otherLocation: Optional[str] = None
