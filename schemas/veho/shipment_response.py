"""
Veho Shipment Response Schema based on OpenAPI spec
"""

import attr
import typing


@attr.s(auto_attribs=True)
class Event:
    """Event - matches OpenAPI spec"""
    eventType: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderEvent:
    """Order Event - matches OpenAPI spec"""
    eventType: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExternalCarrier:
    """External Carrier - matches OpenAPI spec"""
    name: typing.Optional[str] = None
    trackingId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SpecialHandling:
    """Special Handling - matches OpenAPI spec"""
    dryIce: typing.Optional[dict] = None
    hazmat: typing.Optional[dict] = None


@attr.s(auto_attribs=True)
class PackageResponse:
    """Package Response - matches OpenAPI spec"""
    _id: typing.Optional[str] = None
    orderId: typing.Optional[str] = None
    clientId: typing.Optional[str] = None
    pdfShippingLabelLink: typing.Optional[str] = None
    pngShippingLabelLink: typing.Optional[str] = None
    zplShippingLabelLink: typing.Optional[str] = None
    lastEvent: typing.Optional[str] = None
    createdAt: typing.Optional[str] = None
    updatedAt: typing.Optional[str] = None
    trackingId: typing.Optional[str] = None
    eventLog: typing.Optional[typing.List[Event]] = None
    externalCarrier: typing.Optional[ExternalCarrier] = None
    externalShippingLabelLink: typing.Optional[str] = None
    externalId: typing.Optional[str] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    weight: typing.Optional[int] = None
    declaredValue: typing.Optional[float] = None
    description: typing.Optional[str] = None
    barCode: typing.Optional[str] = None
    specialHandling: typing.Optional[SpecialHandling] = None
    scheduledServiceDate: typing.Optional[str] = None
    quoteId: typing.Optional[str] = None
    dispatchDate: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    tenderFacilityId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderAddress:
    """Order Address - matches OpenAPI spec"""
    street: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    apartment: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FromAddress:
    """From Address - matches OpenAPI spec"""
    addressLine1: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderResponse:
    """Veho Order Response - matches OpenAPI spec"""
    
    _id: typing.Optional[str] = None
    rate: typing.Optional[int] = None
    createdAt: typing.Optional[str] = None
    clientId: typing.Optional[str] = None
    lastEvent: typing.Optional[str] = None
    eventLog: typing.Optional[typing.List[OrderEvent]] = None
    serviceType: typing.Optional[str] = None
    destination: typing.Optional[OrderAddress] = None
    fromAddress: typing.Optional[FromAddress] = None
    fromName: typing.Optional[str] = None
    serviceClass: typing.Optional[str] = None
    recipient: typing.Optional[str] = None
    externalId: typing.Optional[str] = None
    merchantId: typing.Optional[str] = None
    company: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    instructions: typing.Optional[str] = None
    slaDeliveryDate: typing.Optional[str] = None
    consumerExpectedServiceDate: typing.Optional[str] = None
    packages: typing.Optional[typing.List[PackageResponse]] = None 
