import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DeliverBetween:
    start: typing.Optional[str] = None
    end: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Address:
    name: typing.Optional[str] = None
    store_number: typing.Optional[int] = None
    street1: typing.Optional[str] = None
    street2: typing.Any = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zip: typing.Optional[int] = None
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Contact:
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Location:
    address: typing.Optional[Address] = jstruct.JStruct[Address]
    contact: typing.Optional[Contact] = jstruct.JStruct[Contact]
    notes: typing.Any = None


@attr.s(auto_attribs=True)
class LocationClass:
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Event:
    name: typing.Optional[str] = None
    occurred_at: typing.Optional[str] = None
    location: typing.Optional[LocationClass] = jstruct.JStruct[LocationClass]


@attr.s(auto_attribs=True)
class Item:
    description: typing.Optional[str] = None
    reference_id: typing.Any = None
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    value: typing.Optional[float] = None
    quantity: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class Options:
    signature_required: typing.Optional[bool] = None
    notifications_enabled: typing.Optional[bool] = None
    over_21__required: typing.Optional[bool] = None
    extra_compensation: typing.Optional[float] = None
    trailer_required: typing.Optional[bool] = None
    decline_insurance: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ShipmentResponse:
    id: typing.Optional[int] = None
    reference_id: typing.Optional[str] = None
    description: typing.Optional[str] = None
    state: typing.Optional[str] = None
    alternate_id_1: typing.Optional[int] = None
    alternate_id_2: typing.Optional[int] = None
    items: typing.Optional[typing.List[Item]] = jstruct.JList[Item]
    pickup_location: typing.Optional[Location] = jstruct.JStruct[Location]
    delivery_location: typing.Optional[Location] = jstruct.JStruct[Location]
    pickup_after: typing.Optional[str] = None
    deliver_between: typing.Optional[DeliverBetween] = jstruct.JStruct[DeliverBetween]
    options: typing.Optional[Options] = jstruct.JStruct[Options]
    tracking_number: typing.Optional[str] = None
    price: typing.Optional[float] = None
    estimated_distance: typing.Optional[float] = None
    events: typing.Optional[typing.List[Event]] = jstruct.JList[Event]
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None
