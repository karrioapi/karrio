import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AssignedTo:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Contact:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomFields:
    custom1: typing.Optional[str] = None
    custom2: typing.Optional[str] = None
    custom3: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Line:
    lineId: typing.Optional[int] = None
    itemId: typing.Optional[int] = None
    serviceId: typing.Any = None
    productVariantId: typing.Any = None
    barcode: typing.Optional[int] = None
    description: typing.Optional[str] = None
    quantity: typing.Optional[int] = None
    status: typing.Optional[str] = None
    itemStatus: typing.Optional[str] = None
    unitPriceExTax: typing.Optional[int] = None
    priceCurrency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Load:
    quantity: typing.Optional[int] = None
    volume: typing.Optional[int] = None
    weight: typing.Optional[int] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class Location:
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ShippingResponse:
    assignedTo: typing.Optional[AssignedTo] = jstruct.JStruct[AssignedTo]
    stopId: typing.Optional[int] = None
    status: typing.Optional[str] = None
    brandId: typing.Any = None
    contact: typing.Optional[Contact] = jstruct.JStruct[Contact]
    name: typing.Optional[str] = None
    address: typing.Optional[str] = None
    location: typing.Optional[Location] = jstruct.JStruct[Location]
    tripDate: typing.Optional[str] = None
    appointmentTime: typing.Optional[str] = None
    timeWindowStart: typing.Any = None
    timeWindowEnd: typing.Any = None
    durationMinutes: typing.Optional[int] = None
    notes: typing.Optional[str] = None
    lastModifiedDate: typing.Optional[str] = None
    customFields: typing.Optional[CustomFields] = jstruct.JStruct[CustomFields]
    type: typing.Any = None
    shipmentId: typing.Optional[int] = None
    load: typing.Optional[Load] = jstruct.JStruct[Load]
    source: typing.Any = None
    sourceReference: typing.Any = None
    customerId: typing.Optional[int] = None
    runNumber: typing.Optional[int] = None
    teamRegionId: typing.Optional[int] = None
    teamMemberInvoiceId: typing.Optional[int] = None
    customerInvoiceId: typing.Optional[int] = None
    arrivalDate: typing.Optional[str] = None
    lines: typing.Optional[typing.List[Line]] = jstruct.JList[Line]
    driverInstructions: typing.Any = None
    oneTimePin: typing.Optional[str] = None
