import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Address:
    addressLocality: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Location:
    address: typing.Optional[Address] = jstruct.JStruct[Address]


@attr.s(auto_attribs=True)
class Status:
    timestamp: typing.Optional[str] = None
    location: typing.Optional[Location] = jstruct.JStruct[Location]
    statusCode: typing.Optional[str] = None
    status: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServiceArea:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Event:
    date: typing.Optional[str] = None
    time: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    location: typing.Optional[Location] = jstruct.JStruct[Location]
    serviceArea: typing.List[ServiceArea] = jstruct.JList[ServiceArea]


@attr.s(auto_attribs=True)
class Shipment:
    shipmentTrackingNumber: typing.Optional[str] = None
    status: typing.Optional[Status] = jstruct.JStruct[Status]
    estimatedTimeOfDelivery: typing.Optional[str] = None
    events: typing.List[Event] = jstruct.JList[Event]


@attr.s(auto_attribs=True)
class TrackingResponse:
    shipments: typing.List[Shipment] = jstruct.JList[Shipment] 