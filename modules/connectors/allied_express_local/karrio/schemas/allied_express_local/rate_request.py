from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ItemType:
    dangerous: Optional[bool] = None
    height: Optional[int] = None
    itemCount: Optional[int] = None
    length: Optional[int] = None
    volume: Optional[float] = None
    weight: Optional[int] = None
    width: Optional[int] = None


@s(auto_attribs=True)
class GeographicAddressType:
    address1: Optional[str] = None
    address2: Optional[str] = None
    country: Optional[str] = None
    postCode: Optional[int] = None
    state: Optional[str] = None
    suburb: Optional[str] = None


@s(auto_attribs=True)
class JobStopsType:
    companyName: Optional[str] = None
    contact: Optional[str] = None
    emailAddress: Optional[str] = None
    geographicAddress: Optional[GeographicAddressType] = JStruct[GeographicAddressType]
    phoneNumber: Optional[str] = None


@s(auto_attribs=True)
class RateRequestType:
    bookedBy: Optional[str] = None
    account: Optional[str] = None
    readyDate: Optional[str] = None
    instructions: Optional[str] = None
    itemCount: Optional[int] = None
    items: List[ItemType] = JList[ItemType]
    jobStopsP: Optional[JobStopsType] = JStruct[JobStopsType]
    jobStopsD: Optional[JobStopsType] = JStruct[JobStopsType]
    referenceNumbers: List[str] = []
    serviceLevel: Optional[str] = None
    volume: Optional[float] = None
    weight: Optional[int] = None
