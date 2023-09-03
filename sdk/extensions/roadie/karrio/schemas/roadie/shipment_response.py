from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DeliverBetween:
    start: Optional[str] = None
    end: Optional[str] = None


@s(auto_attribs=True)
class Address:
    name: Optional[str] = None
    store_number: Optional[int] = None
    street1: Optional[str] = None
    street2: Any = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@s(auto_attribs=True)
class Contact:
    name: Optional[str] = None
    phone: Optional[str] = None


@s(auto_attribs=True)
class Location:
    address: Optional[Address] = JStruct[Address]
    contact: Optional[Contact] = JStruct[Contact]
    notes: Any = None


@s(auto_attribs=True)
class LocationClass:
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@s(auto_attribs=True)
class Event:
    name: Optional[str] = None
    occurred_at: Optional[str] = None
    location: Optional[LocationClass] = JStruct[LocationClass]


@s(auto_attribs=True)
class Item:
    description: Optional[str] = None
    reference_id: Any = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    value: Optional[float] = None
    quantity: Optional[int] = None


@s(auto_attribs=True)
class Options:
    signature_required: Optional[bool] = None
    notifications_enabled: Optional[bool] = None
    over_21_required: Optional[bool] = None
    extra_compensation: Optional[float] = None
    trailer_required: Optional[bool] = None
    decline_insurance: Optional[bool] = None


@s(auto_attribs=True)
class ShipmentResponse:
    id: Optional[int] = None
    reference_id: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None
    alternate_id_1: Optional[int] = None
    alternate_id_2: Optional[int] = None
    items: List[Item] = JList[Item]
    pickup_location: Optional[Location] = JStruct[Location]
    delivery_location: Optional[Location] = JStruct[Location]
    pickup_after: Optional[str] = None
    deliver_between: Optional[DeliverBetween] = JStruct[DeliverBetween]
    options: Optional[Options] = JStruct[Options]
    tracking_number: Optional[str] = None
    price: Optional[float] = None
    estimated_distance: Optional[float] = None
    events: List[Event] = JList[Event]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
