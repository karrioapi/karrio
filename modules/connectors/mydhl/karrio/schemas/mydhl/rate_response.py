import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ExchangeRateType:
    currentExchangeRate: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    baseCurrency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DeliveryCapabilitiesType:
    deliveryTypeCode: typing.Optional[str] = None
    estimatedDeliveryDateAndTime: typing.Optional[str] = None
    destinationServiceAreaCode: typing.Optional[str] = None
    destinationFacilityAreaCode: typing.Optional[str] = None
    deliveryAdditionalDays: typing.Optional[int] = None
    deliveryDayOfWeek: typing.Optional[int] = None
    totalTransitDays: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class BreakdownPriceBreakdownType:
    priceType: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None
    price: typing.Optional[float] = None
    rate: typing.Optional[float] = None
    basePrice: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class DetailedPriceBreakdownBreakdownType:
    name: typing.Optional[str] = None
    serviceCode: typing.Optional[str] = None
    localServiceCode: typing.Optional[str] = None
    typeCode: typing.Optional[str] = None
    serviceTypeCode: typing.Optional[str] = None
    price: typing.Optional[float] = None
    priceCurrency: typing.Optional[str] = None
    isCustomerAgreement: typing.Optional[bool] = None
    isMarketedService: typing.Optional[bool] = None
    isBillingServiceIndicator: typing.Optional[bool] = None
    priceBreakdown: typing.Optional[typing.List[BreakdownPriceBreakdownType]] = jstruct.JList[BreakdownPriceBreakdownType]


@attr.s(auto_attribs=True)
class DetailedPriceBreakdownType:
    currencyType: typing.Optional[str] = None
    priceCurrency: typing.Optional[str] = None
    breakdown: typing.Optional[typing.List[DetailedPriceBreakdownBreakdownType]] = jstruct.JList[DetailedPriceBreakdownBreakdownType]


@attr.s(auto_attribs=True)
class ItemBreakdownType:
    name: typing.Optional[str] = None
    price: typing.Optional[float] = None
    priceBreakdown: typing.Optional[typing.List[BreakdownPriceBreakdownType]] = jstruct.JList[BreakdownPriceBreakdownType]


@attr.s(auto_attribs=True)
class ItemType:
    number: typing.Optional[int] = None
    breakdown: typing.Optional[typing.List[ItemBreakdownType]] = jstruct.JList[ItemBreakdownType]


@attr.s(auto_attribs=True)
class PickupCapabilitiesType:
    nextBusinessDay: typing.Optional[bool] = None
    localCutoffDateAndTime: typing.Optional[str] = None
    GMTCutoffTime: typing.Optional[str] = None
    pickupEarliest: typing.Optional[str] = None
    pickupLatest: typing.Optional[str] = None
    pickupCutoffSameDayOutboundProcessing: typing.Optional[str] = None
    originServiceAreaCode: typing.Optional[str] = None
    originFacilityAreaCode: typing.Optional[str] = None
    pickupAdditionalDays: typing.Optional[int] = None
    pickupDayOfWeek: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ServiceCodeType:
    serviceCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DependencyRuleGroupType:
    dependencyRuleName: typing.Optional[str] = None
    dependencyDescription: typing.Optional[str] = None
    dependencyCondition: typing.Optional[str] = None
    requiredServiceCodes: typing.Optional[typing.List[ServiceCodeType]] = jstruct.JList[ServiceCodeType]


@attr.s(auto_attribs=True)
class ServiceCodeDependencyRuleGroupType:
    dependentServiceCode: typing.Optional[str] = None
    dependencyRuleGroup: typing.Optional[typing.List[DependencyRuleGroupType]] = jstruct.JList[DependencyRuleGroupType]


@attr.s(auto_attribs=True)
class ServiceCodeMutuallyExclusiveGroupType:
    serviceCodeRuleName: typing.Optional[str] = None
    description: typing.Optional[str] = None
    serviceCodes: typing.Optional[typing.List[ServiceCodeType]] = jstruct.JList[ServiceCodeType]


@attr.s(auto_attribs=True)
class TotalPriceType:
    currencyType: typing.Optional[str] = None
    priceCurrency: typing.Optional[str] = None
    price: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class TotalPriceBreakdownPriceBreakdownType:
    typeCode: typing.Optional[str] = None
    price: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class TotalPriceBreakdownType:
    currencyType: typing.Optional[str] = None
    priceCurrency: typing.Optional[str] = None
    priceBreakdown: typing.Optional[typing.List[TotalPriceBreakdownPriceBreakdownType]] = jstruct.JList[TotalPriceBreakdownPriceBreakdownType]


@attr.s(auto_attribs=True)
class WeightType:
    volumetric: typing.Optional[float] = None
    provided: typing.Optional[float] = None
    unitOfMeasurement: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ProductType:
    productName: typing.Optional[str] = None
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    localProductCountryCode: typing.Optional[str] = None
    networkTypeCode: typing.Optional[str] = None
    isCustomerAgreement: typing.Optional[bool] = None
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    totalPrice: typing.Optional[typing.List[TotalPriceType]] = jstruct.JList[TotalPriceType]
    totalPriceBreakdown: typing.Optional[typing.List[TotalPriceBreakdownType]] = jstruct.JList[TotalPriceBreakdownType]
    detailedPriceBreakdown: typing.Optional[typing.List[DetailedPriceBreakdownType]] = jstruct.JList[DetailedPriceBreakdownType]
    serviceCodeMutuallyExclusiveGroups: typing.Optional[typing.List[ServiceCodeMutuallyExclusiveGroupType]] = jstruct.JList[ServiceCodeMutuallyExclusiveGroupType]
    serviceCodeDependencyRuleGroups: typing.Optional[typing.List[ServiceCodeDependencyRuleGroupType]] = jstruct.JList[ServiceCodeDependencyRuleGroupType]
    pickupCapabilities: typing.Optional[PickupCapabilitiesType] = jstruct.JStruct[PickupCapabilitiesType]
    deliveryCapabilities: typing.Optional[DeliveryCapabilitiesType] = jstruct.JStruct[DeliveryCapabilitiesType]
    items: typing.Optional[typing.List[ItemType]] = jstruct.JList[ItemType]
    pricingDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    products: typing.Optional[typing.List[ProductType]] = jstruct.JList[ProductType]
    exchangeRates: typing.Optional[typing.List[ExchangeRateType]] = jstruct.JList[ExchangeRateType]
    warnings: typing.Optional[typing.List[str]] = None
