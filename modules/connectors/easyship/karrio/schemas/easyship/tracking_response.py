import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetaType:
    request_id: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CheckpointType:
    checkpoint_time: typing.Optional[str] = None
    city: typing.Optional[str] = None
    country_iso3: typing.Optional[str] = None
    country_name: typing.Optional[str] = None
    handler: typing.Optional[str] = None
    location: typing.Optional[str] = None
    message: typing.Optional[str] = None
    order_number: typing.Optional[str] = None
    postal_code: typing.Optional[str] = None
    country_alpha2: typing.Optional[str] = None
    description: typing.Optional[str] = None
    primary_status: typing.Optional[str] = None
    state: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CourierType:
    id: typing.Optional[str] = None
    umbrella_name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingType:
    courier: typing.Optional[CourierType] = jstruct.JStruct[CourierType]
    destination_country_alpha2: typing.Optional[str] = None
    easyship_shipment_id: typing.Optional[str] = None
    eta_date: typing.Optional[str] = None
    id: typing.Optional[str] = None
    origin_country_alpha2: typing.Optional[str] = None
    platform_order_number: typing.Optional[str] = None
    source: typing.Optional[str] = None
    status: typing.Optional[str] = None
    tracking_number: typing.Optional[str] = None
    tracking_status: typing.Optional[str] = None
    tracking_page_url: typing.Optional[str] = None
    checkpoints: typing.Optional[typing.List[CheckpointType]] = jstruct.JList[CheckpointType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    meta: typing.Optional[MetaType] = jstruct.JStruct[MetaType]
    tracking: typing.Optional[TrackingType] = jstruct.JStruct[TrackingType]
