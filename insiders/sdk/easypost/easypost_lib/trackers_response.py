from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class CarrierDetail:
    object: Optional[str] = None
    service: Optional[str] = None
    container_type: Optional[str] = None
    est_delivery_date_local: Optional[str] = None
    est_delivery_time_local: Optional[str] = None
    origin_location: Optional[str] = None
    destination_location: Optional[str] = None


@s(auto_attribs=True)
class Fee:
    object: Optional[str] = None
    type: Optional[str] = None
    amount: Optional[str] = None
    charged: Optional[bool] = None
    refunded: Optional[bool] = None


@s(auto_attribs=True)
class TrackingLocation:
    object: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[int] = None


@s(auto_attribs=True)
class TrackingDetail:
    object: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    tracking_detail_datetime: Optional[str] = None
    source: Optional[str] = None
    tracking_location: Optional[TrackingLocation] = JStruct[TrackingLocation]


@s(auto_attribs=True)
class Tracker:
    id: Optional[str] = None
    object: Optional[str] = None
    mode: Optional[str] = None
    tracking_code: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    signed_by: Optional[str] = None
    weight: Optional[float] = None
    est_delivery_date: Optional[str] = None
    shipment_id: Optional[str] = None
    carrier: Optional[str] = None
    public_url: Optional[str] = None
    tracking_details: List[TrackingDetail] = JList[TrackingDetail]
    carrier_detail: Optional[CarrierDetail] = JStruct[CarrierDetail]
    fees: List[Fee] = JList[Fee]


@s(auto_attribs=True)
class TrackersResponse:
    trackers: List[Tracker] = JList[Tracker]
    has_more: Optional[bool] = None
