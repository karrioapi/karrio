import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingLocationElementType:
    """Rich location data — present in partner tracking responses, absent in standard."""

    eventLocation: typing.Optional[str] = None
    street: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zip: typing.Optional[str] = None
    latitude: typing.Optional[str] = None
    longitude: typing.Optional[str] = None
    timezone: typing.Optional[str] = None
    countryId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseElementType:
    """Unified tracking event — handles both standard and partner responses.

    The `location` field is nullable: absent in standard responses, present
    in partner responses with rich address data.
    """

    prefix: typing.Optional[str] = None
    airWaybill: typing.Optional[str] = None
    headerReference: typing.Optional[str] = None
    packageReference: typing.Optional[str] = None
    pieceReference: typing.Optional[str] = None
    eventType: typing.Optional[str] = None
    eventDate: typing.Optional[str] = None
    flightNumber: typing.Optional[str] = None
    flightDate: typing.Optional[str] = None
    eventLocation: typing.Optional[str] = None
    flightSegmentOrigin: typing.Optional[str] = None
    flightSegmentDestination: typing.Optional[str] = None
    pieces: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    description: typing.Optional[str] = None
    referenceAirWaybill: typing.Any = None
    estimatedDeliveryDate: typing.Optional[str] = None
    bagNumber: typing.Optional[str] = None
    subEventType: typing.Any = None
    location: typing.Optional[TrackingLocationElementType] = jstruct.JStruct[TrackingLocationElementType]
