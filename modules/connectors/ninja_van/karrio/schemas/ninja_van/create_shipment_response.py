from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class AddressType:
    address1: Optional[str] = None
    address2: Optional[str] = None
    area: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address_type: Optional[str] = None
    country: Optional[str] = None
    postcode: Optional[int] = None


@s(auto_attribs=True)
class FromType:
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[AddressType] = JStruct[AddressType]


@s(auto_attribs=True)
class TimeslotType:
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    timezone: Optional[str] = None


@s(auto_attribs=True)
class DimensionsType:
    weight: Optional[float] = None


@s(auto_attribs=True)
class ItemType:
    item_description: Optional[str] = None
    quantity: Optional[int] = None
    is_dangerous_good: Optional[bool] = None


@s(auto_attribs=True)
class ParcelJobType:
    is_pickup_required: Optional[bool] = None
    pickup_service_type: Optional[str] = None
    pickup_service_level: Optional[str] = None
    pickup_addressid: Optional[int] = None
    pickup_date: Optional[str] = None
    pickup_timeslot: Optional[TimeslotType] = JStruct[TimeslotType]
    pickup_approximate_volume: Optional[str] = None
    pickup_instructions: Optional[str] = None
    delivery_startdate: Optional[str] = None
    delivery_timeslot: Optional[TimeslotType] = JStruct[TimeslotType]
    delivery_instructions: Optional[str] = None
    allow_weekend_delivery: Optional[bool] = None
    dimensions: Optional[DimensionsType] = JStruct[DimensionsType]
    items: List[ItemType] = JList[ItemType]


@s(auto_attribs=True)
class ReferenceType:
    merchant_order_number: Optional[str] = None


@s(auto_attribs=True)
class CreateShipmentResponseType:
    requested_tracking_number: Optional[str] = None
    tracking_number: Optional[str] = None
    service_type: Optional[str] = None
    service_level: Optional[str] = None
    reference: Optional[ReferenceType] = JStruct[ReferenceType]
    address_from: Optional[FromType] = JStruct[FromType]
    to: Optional[FromType] = JStruct[FromType]
    parcel_job: Optional[ParcelJobType] = JStruct[ParcelJobType]
