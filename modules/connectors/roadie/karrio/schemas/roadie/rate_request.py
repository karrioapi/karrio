import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DeliverBetween:
    start: typing.Optional[str] = None
    end: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Address:
    street1: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zip: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class Location:
    address: typing.Optional[Address] = jstruct.JStruct[Address]


@attr.s(auto_attribs=True)
class Item:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    quantity: typing.Optional[int] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class RateRequest:
    items: typing.Optional[typing.List[Item]] = jstruct.JList[Item]
    pickup_location: typing.Optional[Location] = jstruct.JStruct[Location]
    delivery_location: typing.Optional[Location] = jstruct.JStruct[Location]
    pickup_after: typing.Optional[str] = None
    deliver_between: typing.Optional[DeliverBetween] = jstruct.JStruct[DeliverBetween]
