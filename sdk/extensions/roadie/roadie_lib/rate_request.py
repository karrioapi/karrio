from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DeliverBetween:
    start: Optional[str] = None
    end: Optional[str] = None


@s(auto_attribs=True)
class Address:
    street1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[int] = None


@s(auto_attribs=True)
class Location:
    address: Optional[Address] = JStruct[Address]


@s(auto_attribs=True)
class Item:
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    quantity: Optional[int] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class RateRequest:
    items: List[Item] = JList[Item]
    pickup_location: Optional[Location] = JStruct[Location]
    delivery_location: Optional[Location] = JStruct[Location]
    pickup_after: Optional[str] = None
    deliver_between: Optional[DeliverBetween] = JStruct[DeliverBetween]
