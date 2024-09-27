from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class MetaType:
    request_id: Optional[str] = None


@s(auto_attribs=True)
class CheckpointType:
    checkpoint_time: Optional[str] = None
    city: Optional[str] = None
    country_iso3: Optional[str] = None
    country_name: Optional[str] = None
    handler: Optional[str] = None
    location: Optional[str] = None
    message: Optional[str] = None
    order_number: Optional[str] = None
    postal_code: Optional[str] = None
    country_alpha2: Optional[str] = None
    description: Optional[str] = None
    primary_status: Optional[str] = None
    state: Optional[str] = None


@s(auto_attribs=True)
class CourierType:
    id: Optional[str] = None
    umbrella_name: Optional[str] = None


@s(auto_attribs=True)
class TrackingType:
    courier: Optional[CourierType] = JStruct[CourierType]
    destination_country_alpha2: Optional[str] = None
    easyship_shipment_id: Optional[str] = None
    eta_date: Optional[str] = None
    id: Optional[str] = None
    origin_country_alpha2: Optional[str] = None
    platform_order_number: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_status: Optional[str] = None
    tracking_page_url: Optional[str] = None
    checkpoints: List[CheckpointType] = JList[CheckpointType]


@s(auto_attribs=True)
class TrackingResponseType:
    meta: Optional[MetaType] = JStruct[MetaType]
    tracking: Optional[TrackingType] = JStruct[TrackingType]
