from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Contact:
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


@s(auto_attribs=True)
class CustomFields:
    custom1: Optional[str] = None
    custom2: Optional[str] = None
    custom3: Optional[str] = None


@s(auto_attribs=True)
class Line:
    barcode: Optional[int] = None
    description: Optional[str] = None
    currentLocation: Optional[str] = None
    serviceId: Optional[int] = None
    productVariantId: Optional[int] = None
    quantity: Optional[int] = None


@s(auto_attribs=True)
class Load:
    quantity: Optional[int] = None
    volume: Optional[int] = None
    weight: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


@s(auto_attribs=True)
class Location:
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@s(auto_attribs=True)
class ShippingRequest:
    contact: Optional[Contact] = JStruct[Contact]
    name: Optional[str] = None
    address: Optional[str] = None
    location: Optional[Location] = JStruct[Location]
    type: Any = None
    appointmentTime: Optional[str] = None
    timeWindowStart: Any = None
    timeWindowEnd: Any = None
    brandId: Any = None
    durationMinutes: Optional[int] = None
    notes: Optional[str] = None
    tripDate: Optional[str] = None
    customFields: Optional[CustomFields] = JStruct[CustomFields]
    assignedTeamMemberId: Optional[str] = None
    source: Any = None
    sourceReference: Any = None
    load: Optional[Load] = JStruct[Load]
    customerId: Optional[int] = None
    runNumber: Optional[int] = None
    teamRegionId: Optional[int] = None
    driverInstructions: Any = None
    lines: List[Line] = JList[Line]
