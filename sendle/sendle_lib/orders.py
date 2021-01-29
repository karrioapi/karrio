"""Sendle Orders Datatypes definition module."""

import attr
from typing import Dict
from jstruct import JStruct


@attr.s(auto_attribs=True)
class Parcel:
    pickup_date: str = None
    description: str = None
    kilogram_weight: float = None
    cubic_metre_volume: float = None
    customer_reference: str = None
    metadata: dict = None


@attr.s(auto_attribs=True)
class Contact:
    name: str = None
    email: str = None
    phone: str = None
    company: str = None


@attr.s(auto_attribs=True)
class Address:
    address_line1: str = None
    address_line2: str = None
    suburb: str = None
    postcode: str = None
    state_name: str = None
    country: str = None


@attr.s(auto_attribs=True)
class Sender:
    instructions: str = None
    contact: Contact = JStruct[Contact]
    address: Address = JStruct[Address]


@attr.s(auto_attribs=True)
class Receiver:
    instructions: str = None
    contact: Contact = JStruct[Contact]
    address: Address = JStruct[Address]


@attr.s(auto_attribs=True)
class OrderRequest(Parcel):
    sender: Sender = JStruct[Sender]
    receiver: Receiver = JStruct[Receiver]


@attr.s(auto_attribs=True)
class Route:
    description: str = None
    type: str = None
    delivery_guarantee_status: str = None


@attr.s(auto_attribs=True)
class Scheduling:
    is_cancellable: bool = None
    pickup_date: str = None


@attr.s(auto_attribs=True)
class Price:
    currency: str = None
    amount: float = None


@attr.s(auto_attribs=True)
class OrderResponse(Parcel):
    sender: Sender = JStruct[Sender]
    receiver: Receiver = JStruct[Receiver]
    order_id: str = None
    state: str = None
    order_url: str = None
    sendle_reference: str = None
    tracking_url: str = None
    labels: str = None
    scheduling: Scheduling = JStruct[Scheduling]
    route: Route = JStruct[Route]
    price: Dict[str, Price] = None


@attr.s(auto_attribs=True)
class Contents(Parcel):
    description: str = None
    value: float = None
    country_of_origin: str = None


@attr.s(auto_attribs=True)
class InternationalOrderRequest(Parcel):
    sender: Sender = JStruct[Sender]
    receiver: Receiver = JStruct[Receiver]
    contents: Contents = JStruct[Contents]


@attr.s(auto_attribs=True)
class InternationalOrderResponse(InternationalOrderRequest):
    order_id: str = None
    state: str = None
    order_url: str = None
    sendle_reference: str = None
    tracking_url: str = None
    labels: str = None
    scheduling: Scheduling = JStruct[Scheduling]
