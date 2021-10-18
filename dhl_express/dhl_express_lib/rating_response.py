from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ExchangeRate:
    currentExchangeRate: Optional[float] = None
    currency: Optional[str] = None
    baseCurrency: Optional[str] = None


@s(auto_attribs=True)
class DeliveryCapabilities:
    deliveryTypeCode: Optional[str] = None
    estimatedDeliveryDateAndTime: Optional[str] = None
    destinationServiceAreaCode: Optional[str] = None
    destinationFacilityAreaCode: Optional[str] = None
    deliveryAdditionalDays: Optional[int] = None
    deliveryDayOfWeek: Optional[int] = None
    totalTransitDays: Optional[int] = None


@s(auto_attribs=True)
class BreakdownPriceBreakdown:
    priceType: Optional[str] = None
    typeCode: Optional[str] = None
    price: Optional[int] = None
    rate: Optional[int] = None
    basePrice: Optional[int] = None


@s(auto_attribs=True)
class Breakdown:
    name: Optional[str] = None
    serviceCode: Optional[str] = None
    localServiceCode: Optional[str] = None
    typeCode: Optional[str] = None
    serviceTypeCode: Optional[str] = None
    price: Optional[int] = None
    priceCurrency: Optional[str] = None
    isCustomerAgreement: Optional[bool] = None
    isMarketedService: Optional[bool] = None
    isBillingServiceIndicator: Optional[bool] = None
    priceBreakdown: List[BreakdownPriceBreakdown] = JList[BreakdownPriceBreakdown]
    tariffRateFormula: List[str] = JList[str]


@s(auto_attribs=True)
class DetailedPriceBreakdown:
    currencyType: Optional[str] = None
    priceCurrency: Optional[str] = None
    breakdown: List[Breakdown] = JList[Breakdown]


@s(auto_attribs=True)
class Item:
    number: Optional[int] = None
    breakdown: List[Breakdown] = JList[Breakdown]


@s(auto_attribs=True)
class PickupCapabilities:
    nextBusinessDay: Optional[bool] = None
    localCutoffDateAndTime: Optional[str] = None
    GMTCutoffTime: Optional[str] = None
    pickupEarliest: Optional[str] = None
    pickupLatest: Optional[str] = None
    originServiceAreaCode: Optional[str] = None
    originFacilityAreaCode: Optional[str] = None
    pickupAdditionalDays: Optional[int] = None
    pickupDayOfWeek: Optional[int] = None


@s(auto_attribs=True)
class TotalPrice:
    currencyType: Optional[str] = None
    priceCurrency: Optional[str] = None
    price: Optional[float] = None


@s(auto_attribs=True)
class TotalPriceBreakdownPriceBreakdown:
    typeCode: Optional[str] = None
    price: Optional[float] = None


@s(auto_attribs=True)
class TotalPriceBreakdown:
    currencyType: Optional[str] = None
    priceCurrency: Optional[str] = None
    priceBreakdown: List[TotalPriceBreakdownPriceBreakdown] = JList[TotalPriceBreakdownPriceBreakdown]


@s(auto_attribs=True)
class Weight:
    volumetric: Optional[int] = None
    provided: Optional[float] = None
    unitOfMeasurement: Optional[str] = None


@s(auto_attribs=True)
class Product:
    productName: Optional[str] = None
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    localProductCountryCode: Optional[str] = None
    networkTypeCode: Optional[str] = None
    isCustomerAgreement: Optional[bool] = None
    weight: Optional[Weight] = JStruct[Weight]
    totalPrice: List[TotalPrice] = JList[TotalPrice]
    totalPriceBreakdown: List[TotalPriceBreakdown] = JList[TotalPriceBreakdown]
    detailedPriceBreakdown: List[DetailedPriceBreakdown] = JList[DetailedPriceBreakdown]
    pickupCapabilities: Optional[PickupCapabilities] = JStruct[PickupCapabilities]
    deliveryCapabilities: Optional[DeliveryCapabilities] = JStruct[DeliveryCapabilities]
    items: List[Item] = JList[Item]
    pricingDate: Optional[str] = None


@s(auto_attribs=True)
class RatingResponse:
    products: List[Product] = JList[Product]
    exchangeRates: List[ExchangeRate] = JList[ExchangeRate]
    warnings: List[str] = JList[str]
