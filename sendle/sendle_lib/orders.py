import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Label:
    format: Optional[str] = None
    size: Optional[str] = None
    url: Optional[str] = None


@attr.s(auto_attribs=True)
class Charge:
    currency: Optional[str] = None
    amount: Optional[float] = None


@attr.s(auto_attribs=True)
class Price:
    tax: Optional[Charge] = JStruct[Charge]
    net: Optional[Charge] = JStruct[Charge]
    gross: Optional[Charge] = JStruct[Charge]


@attr.s(auto_attribs=True)
class Address:
    address_line2: Optional[str] = None
    postcode: Optional[int] = None
    address_line1: Optional[str] = None
    suburb: Optional[str] = None
    state_name: Optional[str] = None
    country: Optional[str] = None


@attr.s(auto_attribs=True)
class Contact:
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    sendle_id: Optional[str] = None


@attr.s(auto_attribs=True)
class AddressDetails:
    contact: Optional[Contact] = JStruct[Contact]
    address: Optional[Address] = JStruct[Address]
    instructions: Optional[str] = None


@attr.s(auto_attribs=True)
class Route:
    description: Optional[str] = None
    type: Optional[str] = None
    delivery_guarantee_status: Optional[str] = None


@attr.s(auto_attribs=True)
class Scheduling:
    picked_up_on: Optional[str] = None
    delivered_on: Optional[str] = None
    is_cancellable: Optional[bool] = None
    pickup_date: Optional[str] = None
    estimated_delivery_date_minimum: Optional[str] = None
    estimated_delivery_date_maximum: Optional[str] = None


@attr.s(auto_attribs=True)
class Status:
    description: Optional[str] = None
    last_changed_at: Optional[str] = None


@attr.s(auto_attribs=True)
class Measurement:
    value: Optional[str] = None
    units: Optional[str] = None


@attr.s(auto_attribs=True)
class Order:
    order_id: Optional[str] = None
    state: Optional[str] = None
    status: Optional[Status] = JStruct[Status]
    order_url: Optional[str] = None
    sendle_reference: Optional[str] = None
    tracking_url: Optional[str] = None
    metadata: Optional[dict] = None
    labels: Optional[List[Label]] = JList[Label]
    scheduling: Optional[Scheduling] = JList[Scheduling]
    description: Optional[str] = None
    kilogram_weight: Optional[str] = None
    weight: Optional[Measurement] = JStruct[Measurement]
    cubic_metre_volume: Optional[str] = None
    volume: Optional[Measurement] = JStruct[Measurement]
    customer_reference: Optional[str] = None
    sender: Optional[AddressDetails] = JStruct[AddressDetails]
    receiver: Optional[AddressDetails] = JStruct[AddressDetails]
    route: Optional[Route] = JStruct[Route]
    price: Optional[Price] = JStruct[Price]


@attr.s(auto_attribs=True)
class OrderCancellResponse:
    order_id: Optional[str] = None
    state: Optional[str] = None
    order_url: Optional[str] = None
    sendle_reference: Optional[str] = None
    tracking_url: Optional[str] = None
    customer_reference: Optional[str] = None
    cancelled_at: Optional[str] = None
    cancellation_message: Optional[str] = None


@attr.s(auto_attribs=True)
class Contents:
    description: Optional[str] = None
    value: Optional[str] = None
    country_of_origin: Optional[str] = None


@attr.s(auto_attribs=True)
class OrderRequest:
    pickup_date: Optional[str] = None
    first_mile_option: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[Measurement] = JStruct[Measurement]
    volume: Optional[Measurement] = JStruct[Measurement]
    customer_reference: Optional[str] = None
    metadata: Optional[dict] = None
    sender: Optional[AddressDetails] = JStruct[AddressDetails]
    receiver: Optional[AddressDetails] = JStruct[AddressDetails]
    contents: Optional[Contents] = JStruct[Contents]


@attr.s(auto_attribs=True)
class OrderState:
    state: Optional[str] = None
    status: Optional[Status] = JStruct[Status]
