from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DeliveryChoiceType:
    deliveryChoice: Optional[int] = None


@s(auto_attribs=True)
class ContextDataType:
    deliveryChoice: Optional[DeliveryChoiceType] = JStruct[DeliveryChoiceType]
    originCountry: Optional[str] = None
    arrivalCountry: Optional[str] = None


@s(auto_attribs=True)
class EventType:
    code: Optional[str] = None
    label: Optional[str] = None
    date: Optional[str] = None


@s(auto_attribs=True)
class TimelineType:
    shortLabel: Optional[str] = None
    longLabel: Optional[str] = None
    id: Optional[int] = None
    country: Optional[str] = None
    status: Optional[bool] = None
    type: Optional[int] = None
    date: Optional[str] = None


@s(auto_attribs=True)
class ShipmentType:
    idShip: Optional[str] = None
    holder: Optional[int] = None
    product: Optional[str] = None
    isFinal: Optional[bool] = None
    deliveryDate: Optional[str] = None
    entryDate: Optional[str] = None
    timeline: List[TimelineType] = JList[TimelineType]
    event: List[EventType] = JList[EventType]
    contextData: Optional[ContextDataType] = JStruct[ContextDataType]
    estimDate: Optional[str] = None
    url: Optional[str] = None


@s(auto_attribs=True)
class ResponseType:
    lang: Optional[str] = None
    scope: Optional[str] = None
    returnCode: Optional[int] = None
    shipment: Optional[ShipmentType] = JStruct[ShipmentType]


@s(auto_attribs=True)
class TrackingResponseType:
    responses: List[ResponseType] = JList[ResponseType]
