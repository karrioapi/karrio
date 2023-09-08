from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AssignedTo:
    id: Optional[str] = None
    name: Optional[str] = None


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
    lineId: Optional[int] = None
    itemId: Optional[int] = None
    serviceId: Any = None
    productVariantId: Any = None
    barcode: Optional[int] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    itemStatus: Optional[str] = None
    unitPriceExTax: Optional[int] = None
    priceCurrency: Optional[str] = None


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
class TrackingResponse:
    assignedTo: Optional[AssignedTo] = JStruct[AssignedTo]
    stopId: Optional[int] = None
    status: Optional[str] = None
    brandId: Any = None
    contact: Optional[Contact] = JStruct[Contact]
    name: Optional[str] = None
    address: Optional[str] = None
    location: Optional[Location] = JStruct[Location]
    tripDate: Optional[str] = None
    appointmentTime: Optional[str] = None
    timeWindowStart: Any = None
    timeWindowEnd: Any = None
    durationMinutes: Optional[int] = None
    notes: Optional[str] = None
    lastModifiedDate: Optional[str] = None
    customFields: Optional[CustomFields] = JStruct[CustomFields]
    type: Any = None
    shipmentId: Optional[int] = None
    load: Optional[Load] = JStruct[Load]
    source: Any = None
    sourceReference: Any = None
    customerId: Optional[int] = None
    runNumber: Optional[int] = None
    teamRegionId: Optional[int] = None
    teamMemberInvoiceId: Optional[int] = None
    customerInvoiceId: Optional[int] = None
    arrivalDate: Optional[str] = None
    lines: List[Line] = JList[Line]
    driverInstructions: Any = None
    oneTimePin: Optional[str] = None
