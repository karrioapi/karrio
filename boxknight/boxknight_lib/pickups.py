import attr
from jstruct import JStruct, JList, REQUIRED
from typing import Optional, List


@attr.s(auto_attribs=True)
class Recipient:
    name: str
    phone: str
    notes: Optional[str] = None
    email: Optional[str] = None


@attr.s(auto_attribs=True)
class PickupRequestRecipientAddress:
    street: str
    city: str
    province: str
    country: str
    postalCode: str
    unit: Optional[str] = None


@attr.s(auto_attribs=True)
class PickupRequest:
    packageCount: int
    recipient: Recipient = JStruct[Recipient, REQUIRED]
    recipientAddress: PickupRequestRecipientAddress = JStruct[PickupRequestRecipientAddress, REQUIRED]

    notes: Optional[str] = None
    completeAfter: Optional[int] = None
    completeBefore: Optional[int] = None
    orderIds: Optional[List[str]] = None


@attr.s(auto_attribs=True)
class Location:
    lat: Optional[float] = None
    lng: Optional[float] = None


@attr.s(auto_attribs=True)
class PickupResponseRecipientAddress:
    number: Optional[int] = None
    street: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None
    sublocality: Optional[str] = None
    location: Location = JStruct[Location]


@attr.s(auto_attribs=True)
class PickupResponse:
    id: Optional[str] = None
    createdAt: Optional[str] = None
    createdBy: Optional[str] = None
    merchantId: Optional[str] = None
    completeAfter: Optional[int] = None
    completeBefore: Optional[int] = None
    recipient: Recipient = JStruct[Recipient]
    recipientAddress: PickupResponseRecipientAddress = JStruct[PickupResponseRecipientAddress]
    packageCount: Optional[int] = None
    notes: Optional[str] = None
    orderIds: Optional[List[str]] = None


@attr.s(auto_attribs=True)
class PickupUpdateRequest:
    orderIds: List[str] = JList[str, REQUIRED]
