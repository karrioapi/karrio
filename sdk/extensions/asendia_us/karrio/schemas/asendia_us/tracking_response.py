from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class EventLocationDetailsType:
    addressLine1: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postalCode: Optional[str] = None
    countryIso2: Optional[str] = None
    countryName: Optional[str] = None


@s(auto_attribs=True)
class TrackingDetailEventType:
    eventCode: Optional[str] = None
    eventDescription: Optional[str] = None
    eventLocationDetails: Optional[EventLocationDetailsType] = JStruct[EventLocationDetailsType]
    eventOn: Optional[str] = None


@s(auto_attribs=True)
class DatumType:
    trackingNumberVendor: Optional[str] = None
    customerReferenceNumber: Optional[str] = None
    trackingDetailEvents: List[TrackingDetailEventType] = JList[TrackingDetailEventType]


@s(auto_attribs=True)
class ResponseStatusType:
    responseStatusCode: Optional[int] = None
    responseStatusMessage: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    data: List[DatumType] = JList[DatumType]
    responseStatus: Optional[ResponseStatusType] = JStruct[ResponseStatusType]
