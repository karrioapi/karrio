"""
Veho Shipment Request Schema based on OpenAPI spec
"""

import attr
import typing


@attr.s(auto_attribs=True)
class OrderAddress:
    """Order Address - matches OpenAPI spec"""
    street: str
    city: str
    state: str
    zipCode: str
    apartment: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FromAddress:
    """From Address - matches OpenAPI spec"""
    addressLine1: str
    city: str
    state: str
    zipCode: str
    addressLine2: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SpecialHandling:
    """Special Handling - matches OpenAPI spec"""
    dryIce: typing.Optional[dict] = None
    hazmat: typing.Optional[dict] = None


@attr.s(auto_attribs=True)
class OrderRequestPackage:
    """Order Request Package - matches OpenAPI spec"""
    externalId: typing.Optional[str] = None
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    declaredValue: typing.Optional[float] = None
    barCode: typing.Optional[str] = None
    description: typing.Optional[str] = None
    specialHandling: typing.Optional[SpecialHandling] = None
    quoteId: typing.Optional[str] = None
    dispatchDate: typing.Optional[str] = None
    shipDate: typing.Optional[str] = None
    tenderFacilityId: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OrderRequest:
    """Veho Order Request - matches OpenAPI spec"""
    
    destination: OrderAddress
    recipient: str
    fromAddress: FromAddress
    serviceClass: typing.Optional[str] = "groundPlus"
    externalId: typing.Optional[str] = None
    merchantId: typing.Optional[str] = None
    fromName: typing.Optional[str] = None
    packages: typing.Optional[typing.List[OrderRequestPackage]] = None
    company: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    instructions: typing.Optional[str] = None
    slaDeliveryDate: typing.Optional[str] = None
    consumerExpectedServiceDate: typing.Optional[str] = None
    packageCount: typing.Optional[int] = None 
