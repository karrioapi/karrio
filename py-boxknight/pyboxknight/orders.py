import attr
from jstruct import JStruct, JList, REQUIRED
from typing import Optional, List


@attr.s(auto_attribs=True)
class Location:
    lat: float
    lng: float


@attr.s(auto_attribs=True)
class OrderAddress:
    number: int
    street: str
    city: str
    province: str
    country: str
    postalCode: str
    sublocality: str
    location: Location


@attr.s(auto_attribs=True)
class Recipient:
    name: str
    phone: str
    notes: Optional[str] = None
    email: Optional[str] = None


@attr.s(auto_attribs=True)
class Order:
    id: Optional[str] = None
    createdAt: Optional[str] = None
    createdBy: Optional[str] = None
    merchantId: Optional[str] = None
    orderStatus: Optional[str] = None
    scanningRequired: Optional[bool] = None
    validAddress: Optional[bool] = None
    labelUrl: Optional[str] = None
    pdfLabelUrl: Optional[str] = None
    recipient: Recipient = JStruct[Recipient]
    recipientAddress: OrderAddress = JStruct[OrderAddress]
    originAddress: OrderAddress = JStruct[OrderAddress]
    packageCount: Optional[int] = None
    signatureRequired: Optional[bool] = None
    service: Optional[str] = None
    notes: Optional[str] = None
    refNumber: Optional[str] = None
    completeAfter: Optional[int] = None
    completeBefore: Optional[int] = None
    merchantDisplayName: Optional[str] = None


@attr.s(auto_attribs=True)
class Address:
    street: str
    city: str
    province: str
    country: str
    postalCode: str
    unit: Optional[str] = None


@attr.s(auto_attribs=True)
class OrderRequest:
    packageCount: int
    signatureRequired: bool
    recipient: Recipient = JStruct[Recipient, REQUIRED]
    recipientAddress: Address = JStruct[Address, REQUIRED]
    originAddress: Address = JStruct[Address, REQUIRED]

    service: Optional[str] = None
    notes: Optional[str] = None
    refNumber: Optional[str] = None
    completeAfter: Optional[int] = None
    completeBefore: Optional[int] = None
    merchantDisplayName: Optional[str] = None


@attr.s(auto_attribs=True)
class OrderResponse:
    id: Optional[str] = None


@attr.s(auto_attribs=True)
class OrderUpdateRequest:
    completeAfter: int
    completeBefore: int
