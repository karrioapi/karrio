import attr
import jstruct
import typing


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
    barcode: typing.Optional[int] = None
    description: typing.Optional[str] = None
    currentLocation: typing.Optional[str] = None
    serviceId: typing.Optional[int] = None
    productVariantId: typing.Optional[int] = None
    quantity: typing.Optional[int] = None


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
class ShippingRequest:
    contact: typing.Optional[Contact] = jstruct.JStruct[Contact]
    name: typing.Optional[str] = None
    address: typing.Optional[str] = None
    location: typing.Optional[Location] = jstruct.JStruct[Location]
    type: typing.Any = None
    appointmentTime: typing.Optional[str] = None
    timeWindowStart: typing.Any = None
    timeWindowEnd: typing.Any = None
    brandId: typing.Any = None
    durationMinutes: typing.Optional[int] = None
    notes: typing.Optional[str] = None
    tripDate: typing.Optional[str] = None
    customFields: typing.Optional[CustomFields] = jstruct.JStruct[CustomFields]
    assignedTeamMemberId: typing.Optional[str] = None
    source: typing.Any = None
    sourceReference: typing.Any = None
    load: typing.Optional[Load] = jstruct.JStruct[Load]
    customerId: typing.Optional[int] = None
    runNumber: typing.Optional[int] = None
    teamRegionId: typing.Optional[int] = None
    driverInstructions: typing.Any = None
    lines: typing.Optional[typing.List[Line]] = jstruct.JList[Line]
