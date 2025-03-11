import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EstimatedDelivery:
    date: typing.Optional[str] = None
    startOfEstimatedWindow: typing.Optional[str] = None
    endOfEstimatedWindow: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Event:
    eventCode: typing.Optional[str] = None
    eventName: typing.Optional[str] = None
    eventDateTime: typing.Optional[str] = None
    locationName: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Redelivery:
    href: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Links:
    summary: typing.Optional[Redelivery] = jstruct.JStruct[Redelivery]
    signature: typing.Optional[Redelivery] = jstruct.JStruct[Redelivery]
    redelivery: typing.Optional[Redelivery] = jstruct.JStruct[Redelivery]


@attr.s(auto_attribs=True)
class Signature:
    recipientName: typing.Optional[str] = None
    signatureDateTime: typing.Optional[str] = None
    imageId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InternationalPostalProvider:
    url: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Summary:
    uniqueItemId: typing.Optional[str] = None
    oneDBarcode: typing.Optional[str] = None
    productId: typing.Optional[str] = None
    productName: typing.Optional[str] = None
    productDescription: typing.Optional[str] = None
    productCategory: typing.Optional[str] = None
    destinationCountryCode: typing.Optional[str] = None
    destinationCountryName: typing.Optional[str] = None
    originCountryCode: typing.Optional[str] = None
    originCountryName: typing.Optional[str] = None
    lastEventCode: typing.Optional[str] = None
    lastEventName: typing.Optional[str] = None
    lastEventDateTime: typing.Optional[str] = None
    lastEventLocationName: typing.Optional[str] = None
    statusDescription: typing.Optional[str] = None
    statusCategory: typing.Optional[str] = None
    statusHelpText: typing.Optional[str] = None
    summaryLine: typing.Optional[str] = None
    internationalPostalProvider: typing.Optional[InternationalPostalProvider] = jstruct.JStruct[InternationalPostalProvider]


@attr.s(auto_attribs=True)
class MailPieces:
    mailPieceId: typing.Optional[str] = None
    carrierShortName: typing.Optional[str] = None
    carrierFullName: typing.Optional[str] = None
    summary: typing.Optional[Summary] = jstruct.JStruct[Summary]
    signature: typing.Optional[Signature] = jstruct.JStruct[Signature]
    estimatedDelivery: typing.Optional[EstimatedDelivery] = jstruct.JStruct[EstimatedDelivery]
    events: typing.Optional[typing.List[Event]] = jstruct.JList[Event]
    links: typing.Optional[Links] = jstruct.JStruct[Links]


@attr.s(auto_attribs=True)
class Tracking:
    mailPieces: typing.Optional[MailPieces] = jstruct.JStruct[MailPieces]
