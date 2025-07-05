import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TotalPrice:
    price: typing.Optional[float] = None
    priceCurrency: typing.Optional[str] = None
    priceType: typing.Optional[str] = None
    breakdown: typing.Optional[typing.List["PriceBreakdown"]] = None


@attr.s(auto_attribs=True)
class PriceBreakdown:
    name: typing.Optional[str] = None
    price: typing.Optional[float] = None
    priceCurrency: typing.Optional[str] = None
    priceType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryCapabilities:
    deliveryTypeCode: typing.Optional[str] = None
    estimatedDeliveryDateAndTime: typing.Optional[str] = None
    destinationServiceAreaCode: typing.Optional[str] = None
    destinationFacilityAreaCode: typing.Optional[str] = None
    deliveryAdditionalDays: typing.Optional[int] = None
    deliveryDayOfWeek: typing.Optional[int] = None
    totalTransitDays: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupCapabilities:
    nextBusinessDay: typing.Optional[bool] = None
    requestedPickupTimeEarliest: typing.Optional[str] = None
    requestedPickupTimeLatest: typing.Optional[str] = None
    originServiceAreaCode: typing.Optional[str] = None
    originFacilityAreaCode: typing.Optional[str] = None
    pickupEarliest: typing.Optional[str] = None
    pickupLatest: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Product:
    name: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    productType: typing.Optional[str] = None
    localProductCountryCode: typing.Optional[str] = None
    deliveryCapabilities: typing.Optional[DeliveryCapabilities] = None
    totalPrice: typing.Optional[typing.List[TotalPrice]] = None
    pickupCapabilities: typing.Optional[PickupCapabilities] = None


@attr.s(auto_attribs=True)
class RateResponse:
    products: typing.Optional[typing.List[Product]] = None 