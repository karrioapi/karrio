import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetaType:
    available_balance: typing.Optional[int] = None
    easyship_shipment_ids: typing.Optional[typing.List[str]] = None
    request_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DefaultForType:
    billing: typing.Optional[bool] = None
    pickup: typing.Optional[bool] = None
    default_for_return: typing.Optional[bool] = None
    sender: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class HkDistrictType:
    area: typing.Optional[str] = None
    district: typing.Optional[str] = None
    id: typing.Optional[int] = None
    zone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ComparisonType:
    changes: typing.Optional[str] = None
    post: typing.Optional[str] = None
    pre: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ValidationType:
    detail: typing.Optional[str] = None
    status: typing.Optional[str] = None
    comparison: typing.Optional[ComparisonType] = jstruct.JStruct[ComparisonType]


@attr.s(auto_attribs=True)
class AddressType:
    city: typing.Optional[str] = None
    company_name: typing.Optional[str] = None
    contact_email: typing.Optional[str] = None
    contact_name: typing.Optional[str] = None
    contact_phone: typing.Optional[str] = None
    country_alpha2: typing.Optional[str] = None
    default_for: typing.Optional[DefaultForType] = jstruct.JStruct[DefaultForType]
    hk_district: typing.Optional[HkDistrictType] = jstruct.JStruct[HkDistrictType]
    id: typing.Optional[str] = None
    line_1: typing.Optional[str] = None
    line_2: typing.Optional[str] = None
    postal_code: typing.Optional[str] = None
    state: typing.Optional[str] = None
    validation: typing.Optional[ValidationType] = jstruct.JStruct[ValidationType]


@attr.s(auto_attribs=True)
class CourierType:
    id: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    courier: typing.Optional[CourierType] = jstruct.JStruct[CourierType]
    easyship_pickup_id: typing.Optional[str] = None
    pickup_fee: typing.Optional[int] = None
    pickup_reference_number: typing.Optional[str] = None
    pickup_state: typing.Optional[str] = None
    provider_name: typing.Optional[str] = None
    selected_from_time: typing.Optional[str] = None
    selected_to_time: typing.Optional[str] = None
    shipments_count: typing.Optional[int] = None
    total_actual_weight: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class PickupResponseType:
    meta: typing.Optional[MetaType] = jstruct.JStruct[MetaType]
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
