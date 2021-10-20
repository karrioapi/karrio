from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Label:
    format: Optional[str] = None
    size: Optional[str] = None
    url: Optional[str] = None


@s(auto_attribs=True)
class Metadata:
    your_data: Optional[str] = None


@s(auto_attribs=True)
class Gross:
    currency: Optional[str] = None
    amount: Optional[float] = None


@s(auto_attribs=True)
class Price:
    tax: Optional[Gross] = JStruct[Gross]
    net: Optional[Gross] = JStruct[Gross]
    gross: Optional[Gross] = JStruct[Gross]


@s(auto_attribs=True)
class Address:
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    suburb: Optional[str] = None
    state_name: Optional[str] = None
    postcode: Optional[int] = None
    country: Optional[str] = None


@s(auto_attribs=True)
class Contact:
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    sendle_id: Optional[str] = None


@s(auto_attribs=True)
class Receiver:
    contact: Optional[Contact] = JStruct[Contact]
    address: Optional[Address] = JStruct[Address]
    instructions: Optional[str] = None


@s(auto_attribs=True)
class Route:
    description: Optional[str] = None
    type: Optional[str] = None
    delivery_guarantee_status: Optional[str] = None


@s(auto_attribs=True)
class Scheduling:
    is_cancellable: Optional[bool] = None
    pickup_date: Optional[str] = None
    picked_up_on: Optional[str] = None
    delivered_on: Optional[str] = None
    estimated_delivery_date_minimum: Optional[str] = None
    estimated_delivery_date_maximum: Optional[str] = None


@s(auto_attribs=True)
class Status:
    description: Optional[str] = None
    last_changed_at: Optional[str] = None


@s(auto_attribs=True)
class Volume:
    value: Optional[str] = None
    units: Optional[str] = None


@s(auto_attribs=True)
class OrderResponse:
    order_id: Optional[str] = None
    state: Optional[str] = None
    status: Optional[Status] = JStruct[Status]
    order_url: Optional[str] = None
    sendle_reference: Optional[str] = None
    tracking_url: Optional[str] = None
    metadata: Optional[Metadata] = JStruct[Metadata]
    labels: List[Label] = JList[Label]
    scheduling: Optional[Scheduling] = JStruct[Scheduling]
    description: Optional[str] = None
    kilogram_weight: Optional[str] = None
    weight: Optional[Volume] = JStruct[Volume]
    cubic_metre_volume: Optional[str] = None
    volume: Optional[Volume] = JStruct[Volume]
    customer_reference: Optional[str] = None
    sender: Optional[Receiver] = JStruct[Receiver]
    receiver: Optional[Receiver] = JStruct[Receiver]
    route: Optional[Route] = JStruct[Route]
    price: Optional[Price] = JStruct[Price]
