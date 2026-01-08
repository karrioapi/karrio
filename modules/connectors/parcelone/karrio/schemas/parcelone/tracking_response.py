"""ParcelOne TrackLMC REST API v1 - Response Types."""

import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingEventType:
    """Single tracking event."""

    DateTime: typing.Optional[str] = None
    Location: typing.Optional[str] = None
    Status: typing.Optional[str] = None
    StatusCode: typing.Optional[str] = None
    Description: typing.Optional[str] = None
    Carrier: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResultType:
    """Tracking result with events."""

    TrackingID: typing.Optional[str] = None
    CarrierIDLMC: typing.Optional[str] = None
    CarrierTrackingID: typing.Optional[str] = None
    Status: typing.Optional[str] = None
    StatusCode: typing.Optional[str] = None
    DeliveryDate: typing.Optional[str] = None
    EstimatedDelivery: typing.Optional[str] = None
    SignedBy: typing.Optional[str] = None
    Events: typing.Optional[typing.List[TrackingEventType]] = jstruct.JList[TrackingEventType]


@attr.s(auto_attribs=True)
class TrackingResponseType:
    """TrackLMC API response."""

    status: typing.Optional[int] = None
    success: typing.Optional[int] = None
    message: typing.Optional[str] = None
    type: typing.Optional[str] = None
    instance: typing.Optional[str] = None
    results: typing.Optional[TrackingResultType] = jstruct.JStruct[TrackingResultType]
    UniqId: typing.Optional[str] = None
