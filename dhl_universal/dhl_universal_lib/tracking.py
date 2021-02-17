import attr
from jstruct import JList, JStruct
from typing import Optional, List


@attr.s(auto_attribs=True)
class Error:
    title: Optional[str] = None
    detail: Optional[str] = None
    status: Optional[int] = None
    instance: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingRequest:
    trackingNumber: Optional[str] = None
    service: Optional[str] = None
    requesterCountryCode: Optional[str] = None
    originCountryCode: Optional[str] = None
    recipientPostalCode: Optional[str] = None
    language: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


@attr.s(auto_attribs=True)
class Address:
    countryCode: Optional[str] = None
    postalCode: Optional[str] = None
    addressLocality: Optional[str] = None


@attr.s(auto_attribs=True)
class Location:
    address: Optional[Address] = JStruct[Address]


@attr.s(auto_attribs=True)
class EstimatedDeliveryTimeFrame:
    estimatedFrom: Optional[str] = None
    estimatedThrough: Optional[str] = None


@attr.s(auto_attribs=True)
class Status:
    timestamp: Optional[str] = None
    location: Location = JStruct[Location]
    statusCode: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    remark: Optional[str] = None
    nextSteps: Optional[str] = None


@attr.s(auto_attribs=True)
class Shipment:
    id: Optional[str] = None
    service: Optional[str] = None
    origin: Location = JStruct[Location]
    destination: Location = JStruct[Location]
    status: Status = JStruct[Status]
    estimatedTimeOfDelivery: Optional[str] = None
    estimatedDeliveryTimeFrame: EstimatedDeliveryTimeFrame = JStruct[EstimatedDeliveryTimeFrame]
    estimatedTimeOfDeliveryRemark: Optional[str] = None
    serviceUrl: Optional[str] = None
    rerouteUrl: Optional[str] = None
    details: Optional[dict] = None
    events: List[Status] = JList[Status]


@attr.s(auto_attribs=True)
class TrackingResponse:
    url: Optional[str] = None
    prevUrl: Optional[str] = None
    nextUrl: Optional[str] = None
    firstUrl: Optional[str] = None
    lastUrl: Optional[str] = None
    shipments: List[Shipment] = JList[Shipment]
    possibleAdditionalShipmentsUrl: List[str] = JList[str]
