import attr
from typing import Optional, List
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class EstimatedDelivery:
    date: Optional[str] = None
    startOfEstimatedWindow: Optional[str] = None
    endOfEstimatedWindow: Optional[str] = None


@attr.s(auto_attribs=True)
class Event:
    eventCode: Optional[str] = None
    eventName: Optional[str] = None
    eventDateTime: Optional[str] = None
    locationName: Optional[str] = None


@attr.s(auto_attribs=True)
class Link:
    href: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


@attr.s(auto_attribs=True)
class Links:
    summary: Optional[Link] = JStruct[Link]
    signature: Optional[Link] = JStruct[Link]
    redelivery: Optional[Link] = JStruct[Link]


@attr.s(auto_attribs=True)
class Signature:
    recipientName: Optional[str] = None
    signatureDateTime: Optional[str] = None
    imageId: Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalPostalProvider:
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


@attr.s(auto_attribs=True)
class Summary:
    uniqueItemId: Optional[str] = None
    oneDBarcode: Optional[str] = None
    productId: Optional[str] = None
    productName: Optional[str] = None
    productDescription: Optional[str] = None
    productCategory: Optional[str] = None
    destinationCountryCode: Optional[str] = None
    destinationCountryName: Optional[str] = None
    originCountryCode: Optional[str] = None
    originCountryName: Optional[str] = None
    lastEventCode: Optional[str] = None
    lastEventName: Optional[str] = None
    lastEventDateTime: Optional[str] = None
    lastEventLocationName: Optional[str] = None
    statusDescription: Optional[str] = None
    statusCategory: Optional[str] = None
    statusHelpText: Optional[str] = None
    summaryLine: Optional[str] = None
    internationalPostalProvider: Optional[InternationalPostalProvider] = JStruct[InternationalPostalProvider]


@attr.s(auto_attribs=True)
class MailPieces:
    mailPieceId: Optional[str] = None
    carrierShortName: Optional[str] = None
    carrierFullName: Optional[str] = None
    summary: Optional[Summary] = None
    signature: Optional[Signature] = None
    estimatedDelivery: Optional[EstimatedDelivery] = JStruct[EstimatedDelivery]
    events: Optional[List[Event]] = JList[Event]
    links: Optional[Links] = JStruct[Links]


@attr.s(auto_attribs=True)
class TrackingResponse:
    mailPieces: Optional[MailPieces] = None
