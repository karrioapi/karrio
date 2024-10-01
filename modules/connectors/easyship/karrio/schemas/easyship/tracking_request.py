from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ComparisonType:
    changes: Optional[str] = None
    post: Optional[str] = None
    pre: Optional[str] = None


@s(auto_attribs=True)
class ValidationType:
    detail: Optional[str] = None
    status: Optional[str] = None
    comparison: Optional[ComparisonType] = JStruct[ComparisonType]


@s(auto_attribs=True)
class NAddressType:
    city: Optional[str] = None
    company_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    country_alpha2: Optional[str] = None
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    validation: Optional[ValidationType] = JStruct[ValidationType]


@s(auto_attribs=True)
class ItemType:
    description: Optional[str] = None
    quantity: Optional[int] = None


@s(auto_attribs=True)
class TrackingRequestType:
    destination_address: Optional[NAddressType] = JStruct[NAddressType]
    origin_address: Optional[NAddressType] = JStruct[NAddressType]
    courier_id: Optional[str] = None
    origin_address_id: Optional[str] = None
    platform_order_number: Optional[int] = None
    items: List[ItemType] = JList[ItemType]
    tracking_number: Optional[int] = None
