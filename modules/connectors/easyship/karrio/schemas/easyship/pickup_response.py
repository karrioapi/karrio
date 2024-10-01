from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class MetaType:
    available_balance: Optional[int] = None
    easyship_shipment_ids: List[str] = []
    request_id: Optional[str] = None


@s(auto_attribs=True)
class DefaultForType:
    billing: Optional[bool] = None
    pickup: Optional[bool] = None
    default_for_return: Optional[bool] = None
    sender: Optional[bool] = None


@s(auto_attribs=True)
class HkDistrictType:
    area: Optional[str] = None
    district: Optional[str] = None
    id: Optional[int] = None
    zone: Optional[str] = None


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
class AddressType:
    city: Optional[str] = None
    company_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    country_alpha2: Optional[str] = None
    default_for: Optional[DefaultForType] = JStruct[DefaultForType]
    hk_district: Optional[HkDistrictType] = JStruct[HkDistrictType]
    id: Optional[str] = None
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    validation: Optional[ValidationType] = JStruct[ValidationType]


@s(auto_attribs=True)
class CourierType:
    id: Optional[str] = None
    name: Optional[str] = None


@s(auto_attribs=True)
class PickupType:
    address: Optional[AddressType] = JStruct[AddressType]
    courier: Optional[CourierType] = JStruct[CourierType]
    easyship_pickup_id: Optional[str] = None
    pickup_fee: Optional[int] = None
    pickup_reference_number: Optional[str] = None
    pickup_state: Optional[str] = None
    provider_name: Optional[str] = None
    selected_from_time: Optional[str] = None
    selected_to_time: Optional[str] = None
    shipments_count: Optional[int] = None
    total_actual_weight: Optional[float] = None


@s(auto_attribs=True)
class PickupResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    pickup: Optional[PickupType] = JStruct[PickupType]
