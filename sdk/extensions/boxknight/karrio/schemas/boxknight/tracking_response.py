from attr import s
from typing import Optional
from jstruct import JStruct


@s(auto_attribs=True)
class Location:
    lat: Optional[float] = None
    lng: Optional[float] = None


@s(auto_attribs=True)
class Address:
    number: Optional[int] = None
    street: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None
    sublocality: Optional[str] = None
    location: Optional[Location] = JStruct[Location]


@s(auto_attribs=True)
class Recipient:
    name: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    email: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponse:
    id: Optional[str] = None
    createdAt: Optional[str] = None
    createdBy: Optional[str] = None
    merchantId: Optional[str] = None
    orderStatus: Optional[str] = None
    scanningRequired: Optional[bool] = None
    validAddress: Optional[bool] = None
    labelUrl: Optional[str] = None
    pdfLabelUrl: Optional[str] = None
    recipient: Optional[Recipient] = JStruct[Recipient]
    recipientAddress: Optional[Address] = JStruct[Address]
    originAddress: Optional[Address] = JStruct[Address]
    packageCount: Optional[int] = None
    signatureRequired: Optional[bool] = None
    service: Optional[str] = None
    notes: Optional[str] = None
    refNumber: Optional[str] = None
    completeAfter: Optional[int] = None
    completeBefore: Optional[int] = None
    merchantDisplayName: Optional[str] = None
