import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingLocation:
    object: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    country: typing.Optional[str] = None
    zip: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CarrierDetail:
    object: typing.Optional[str] = None
    service: typing.Optional[str] = None
    container_type: typing.Optional[str] = None
    est_delivery_date_local: typing.Optional[str] = None
    est_delivery_time_local: typing.Optional[str] = None
    origin_location: typing.Optional[str] = None
    origin_tracking_location: typing.Optional[TrackingLocation] = jstruct.JStruct[TrackingLocation]
    destination_location: typing.Optional[str] = None
    destination_tracking_location: typing.Optional[str] = None
    guaranteed_delivery_date: typing.Optional[str] = None
    alternate_identifier: typing.Optional[str] = None
    initial_delivery_attempt: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Fee:
    object: typing.Optional[str] = None
    type: typing.Optional[str] = None
    amount: typing.Optional[str] = None
    charged: typing.Optional[bool] = None
    refunded: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class TrackingDetail:
    object: typing.Optional[str] = None
    message: typing.Optional[str] = None
    description: typing.Optional[str] = None
    status: typing.Optional[str] = None
    status_detail: typing.Optional[str] = None
    tracking_detail_datetime: typing.Optional[str] = None
    source: typing.Optional[str] = None
    carrier_code: typing.Optional[str] = None
    tracking_location: typing.Optional[TrackingLocation] = jstruct.JStruct[TrackingLocation]


@attr.s(auto_attribs=True)
class Tracker:
    id: typing.Optional[str] = None
    object: typing.Optional[str] = None
    mode: typing.Optional[str] = None
    tracking_code: typing.Optional[str] = None
    status: typing.Optional[str] = None
    status_detail: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    updated_at: typing.Optional[str] = None
    signed_by: typing.Optional[str] = None
    weight: typing.Optional[str] = None
    est_delivery_date: typing.Optional[str] = None
    shipment_id: typing.Optional[str] = None
    carrier: typing.Optional[str] = None
    tracking_details: typing.Optional[typing.List[TrackingDetail]] = jstruct.JList[TrackingDetail]
    carrier_detail: typing.Optional[CarrierDetail] = jstruct.JStruct[CarrierDetail]
    finalized: typing.Optional[bool] = None
    is_return: typing.Optional[bool] = None
    public_url: typing.Optional[str] = None
    fees: typing.Optional[typing.List[Fee]] = jstruct.JList[Fee]


@attr.s(auto_attribs=True)
class TrackersResponse:
    trackers: typing.Optional[typing.List[Tracker]] = jstruct.JList[Tracker]
    has_more: typing.Optional[bool] = None
