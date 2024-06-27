from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class ExchangeRateType:
    currentExchangeRate: Optional[float] = None
    currency: Optional[str] = None
    baseCurrency: Optional[str] = None


@s(auto_attribs=True)
class DeliveryCapabilitiesType:
    deliveryTypeCode: Optional[str] = None
    estimatedDeliveryDateAndTime: Optional[str] = None
    destinationServiceAreaCode: Optional[str] = None
    destinationFacilityAreaCode: Optional[str] = None
    deliveryAdditionalDays: Optional[int] = None
    deliveryDayOfWeek: Optional[int] = None
    totalTransitDays: Optional[int] = None


@s(auto_attribs=True)
class BreakdownPriceBreakdownType:
    priceType: Optional[str] = None
    typeCode: Optional[str] = None
    price: Optional[int] = None
    rate: Optional[int] = None
    basePrice: Optional[float] = None


@s(auto_attribs=True)
class BreakdownType:
    name: Optional[str] = None
    price: Optional[float] = None
    priceBreakdown: List[BreakdownPriceBreakdownType] = JList[BreakdownPriceBreakdownType]
    serviceCode: Optional[str] = None
    localServiceCode: Optional[str] = None
    serviceTypeCode: Optional[str] = None
    isCustomerAgreement: Optional[bool] = None
    isMarketedService: Optional[bool] = None
    typeCode: Optional[str] = None


@s(auto_attribs=True)
class DetailedPriceBreakdownType:
    currencyType: Optional[str] = None
    priceCurrency: Optional[str] = None
    breakdown: List[BreakdownType] = JList[BreakdownType]


@s(auto_attribs=True)
class PickupCapabilitiesType:
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
class TotalPriceType:
    currencyType: Optional[str] = None
    priceCurrency: Optional[str] = None
    price: Optional[float] = None


@s(auto_attribs=True)
class TotalPriceBreakdownPriceBreakdownType:
    typeCode: Optional[str] = None
    price: Optional[float] = None


@s(auto_attribs=True)
class TotalPriceBreakdownType:
    currencyType: Optional[str] = None
    priceCurrency: Optional[str] = None
    priceBreakdown: List[TotalPriceBreakdownPriceBreakdownType] = JList[TotalPriceBreakdownPriceBreakdownType]


@s(auto_attribs=True)
class WeightType:
    volumetric: Optional[float] = None
    provided: Optional[float] = None
    unitOfMeasurement: Optional[str] = None


@s(auto_attribs=True)
class ProductType:
    productName: Optional[str] = None
    productCode: Optional[str] = None
    localProductCode: Optional[str] = None
    localProductCountryCode: Optional[str] = None
    networkTypeCode: Optional[str] = None
    isCustomerAgreement: Optional[bool] = None
    weight: Optional[WeightType] = JStruct[WeightType]
    totalPrice: List[TotalPriceType] = JList[TotalPriceType]
    totalPriceBreakdown: List[TotalPriceBreakdownType] = JList[TotalPriceBreakdownType]
    detailedPriceBreakdown: List[DetailedPriceBreakdownType] = JList[DetailedPriceBreakdownType]
    pickupCapabilities: Optional[PickupCapabilitiesType] = JStruct[PickupCapabilitiesType]
    deliveryCapabilities: Optional[DeliveryCapabilitiesType] = JStruct[DeliveryCapabilitiesType]
    pricingDate: Optional[str] = None


@s(auto_attribs=True)
class RatingResponseType:
    products: List[ProductType] = JList[ProductType]
    exchangeRates: List[ExchangeRateType] = JList[ExchangeRateType]
