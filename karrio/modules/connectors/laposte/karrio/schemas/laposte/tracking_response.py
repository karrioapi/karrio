import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DeliveryChoice:
    deliveryChoice: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ContextData:
    deliveryChoice: typing.Optional[DeliveryChoice] = jstruct.JStruct[DeliveryChoice]
    originCountry: typing.Optional[str] = None
    arrivalCountry: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Event:
    code: typing.Optional[str] = None
    label: typing.Optional[str] = None
    date: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Timeline:
    shortLabel: typing.Optional[str] = None
    longLabel: typing.Optional[str] = None
    id: typing.Optional[int] = None
    country: typing.Optional[str] = None
    status: typing.Optional[bool] = None
    type: typing.Optional[int] = None
    date: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Shipment:
    idShip: typing.Optional[str] = None
    holder: typing.Optional[int] = None
    product: typing.Optional[str] = None
    isFinal: typing.Optional[bool] = None
    deliveryDate: typing.Optional[str] = None
    entryDate: typing.Optional[str] = None
    timeline: typing.Optional[typing.List[Timeline]] = jstruct.JList[Timeline]
    event: typing.Optional[typing.List[Event]] = jstruct.JList[Event]
    contextData: typing.Optional[ContextData] = jstruct.JStruct[ContextData]
    estimDate: typing.Optional[str] = None
    url: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Response:
    lang: typing.Optional[str] = None
    scope: typing.Optional[str] = None
    returnCode: typing.Optional[int] = None
    shipment: typing.Optional[Shipment] = jstruct.JStruct[Shipment]


@attr.s(auto_attribs=True)
class TrackingResponse:
    responses: typing.Optional[typing.List[Response]] = jstruct.JList[Response]
