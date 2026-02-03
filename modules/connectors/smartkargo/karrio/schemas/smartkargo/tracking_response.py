import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackingResponseElementType:
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
