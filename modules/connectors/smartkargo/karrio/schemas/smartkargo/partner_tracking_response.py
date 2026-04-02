import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PartnerTrackingLocationElementType:
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
class PartnerTrackingResponseElementType:
    headerReference: typing.Optional[str] = None
    packageReference: typing.Optional[str] = None
    pieceReference: typing.Optional[str] = None
    eventDate: typing.Optional[str] = None
    flightNumber: typing.Optional[str] = None
    flightDate: typing.Optional[str] = None
    eventLocation: typing.Optional[str] = None
    flightSegmentOrigin: typing.Optional[str] = None
    flightSegmentDestination: typing.Optional[str] = None
    pieces: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    description: typing.Optional[str] = None
    prefix: typing.Optional[str] = None
    airWaybill: typing.Optional[str] = None
    eventType: typing.Optional[str] = None
    location: typing.Optional[PartnerTrackingLocationElementType] = jstruct.JStruct[PartnerTrackingLocationElementType]
    estimatedDeliveryDate: typing.Optional[str] = None
