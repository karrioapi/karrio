from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class EventLocationDetails:
    addressLine1: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postalCode: Optional[str] = None
    countryIso2: Optional[str] = None
    countryName: Optional[str] = None


@s(auto_attribs=True)
class TrackingDetailEvent:
    eventCode: Optional[str] = None
    eventDescription: Optional[str] = None
    eventLocationDetails: Optional[EventLocationDetails] = JStruct[EventLocationDetails]
    eventOn: Optional[str] = None


@s(auto_attribs=True)
class Datum:
    trackingNumberVendor: Optional[str] = None
    customerReferenceNumber: Optional[str] = None
    trackingDetailEvents: List[TrackingDetailEvent] = JList[TrackingDetailEvent]


@s(auto_attribs=True)
class ResponseStatus:
    responseStatusCode: Optional[int] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class Response:
    data: List[Datum] = JList[Datum]
    responseStatus: Optional[ResponseStatus] = JStruct[ResponseStatus]


@s(auto_attribs=True)
class TrackingDetails:
    response: Optional[Response] = JStruct[Response]
