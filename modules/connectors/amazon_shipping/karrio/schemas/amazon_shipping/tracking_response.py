import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Location:
    city: typing.Optional[str] = None
    stateOrRegion: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class EventHistory:
    eventCode: typing.Optional[str] = None
    location: typing.Optional[Location] = jstruct.JStruct[Location]
    eventTime: typing.Optional[str] = None
    shipmentType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryLocationCoordinates:
    latitude: typing.Optional[float] = None
    longitude: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ProofOfDelivery:
    deliveryLocationCoordinates: typing.Optional[DeliveryLocationCoordinates] = jstruct.JStruct[DeliveryLocationCoordinates]
    deliveryImageURL: typing.Any = None
    receivedBy: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingDetailCodes:
    forward: typing.Optional[typing.List[str]] = None
    returns: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class Summary:
    status: typing.Optional[str] = None
    trackingDetailCodes: typing.Optional[TrackingDetailCodes] = jstruct.JStruct[TrackingDetailCodes]
    proofOfDelivery: typing.Optional[ProofOfDelivery] = jstruct.JStruct[ProofOfDelivery]


@attr.s(auto_attribs=True)
class Payload:
    trackingId: typing.Optional[str] = None
    alternateLegTrackingId: typing.Any = None
    eventHistory: typing.Optional[typing.List[EventHistory]] = jstruct.JList[EventHistory]
    promisedDeliveryDate: typing.Optional[str] = None
    summary: typing.Optional[Summary] = jstruct.JStruct[Summary]


@attr.s(auto_attribs=True)
class TrackingResponse:
    payload: typing.Optional[Payload] = jstruct.JStruct[Payload]
