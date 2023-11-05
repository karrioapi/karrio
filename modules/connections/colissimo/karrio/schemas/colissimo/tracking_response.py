from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DeliveryChoice:
    deliveryChoice: Optional[int] = None


@s(auto_attribs=True)
class ContextData:
    deliveryChoice: Optional[DeliveryChoice] = JStruct[DeliveryChoice]
    originCountry: Optional[str] = None
    arrivalCountry: Optional[str] = None


@s(auto_attribs=True)
class Event:
    code: Optional[str] = None
    label: Optional[str] = None
    date: Optional[str] = None


@s(auto_attribs=True)
class Timeline:
    shortLabel: Optional[str] = None
    longLabel: Optional[str] = None
    id: Optional[int] = None
    country: Optional[str] = None
    status: Optional[bool] = None
    type: Optional[int] = None
    date: Optional[str] = None


@s(auto_attribs=True)
class Shipment:
    idShip: Optional[str] = None
    holder: Optional[int] = None
    product: Optional[str] = None
    isFinal: Optional[bool] = None
    deliveryDate: Optional[str] = None
    entryDate: Optional[str] = None
    timeline: List[Timeline] = JList[Timeline]
    event: List[Event] = JList[Event]
    contextData: Optional[ContextData] = JStruct[ContextData]
    estimDate: Optional[str] = None
    url: Optional[str] = None


@s(auto_attribs=True)
class Response:
    lang: Optional[str] = None
    scope: Optional[str] = None
    returnCode: Optional[int] = None
    shipment: Optional[Shipment] = JStruct[Shipment]


@s(auto_attribs=True)
class TrackingResponse:
    responses: List[Response] = JList[Response]
