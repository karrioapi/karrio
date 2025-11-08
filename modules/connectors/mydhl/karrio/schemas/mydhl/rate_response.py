import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DeliveryCapabilitiesType:
    deliveryTypeCode: typing.Optional[str] = None
    estimatedDeliveryDateAndTime: typing.Optional[str] = None
    destinationServiceAreaCode: typing.Optional[str] = None
    destinationFacilityAreaCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BreakdownType:
    name: typing.Optional[str] = None
    serviceCode: typing.Optional[str] = None
    price: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class DetailedPriceBreakdownType:
    currencyType: typing.Optional[str] = None
    priceCurrency: typing.Optional[str] = None
    breakdown: typing.Optional[typing.List[BreakdownType]] = jstruct.JList[BreakdownType]


@attr.s(auto_attribs=True)
class PickupCapabilitiesType:
    nextBusinessDay: typing.Optional[bool] = None
    localCutoffDateAndTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TotalPriceType:
    currencyType: typing.Optional[str] = None
    priceCurrency: typing.Optional[str] = None
    price: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class PriceBreakdownType:
    typeCode: typing.Optional[str] = None
    price: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class TotalPriceBreakdownType:
    currencyType: typing.Optional[str] = None
    priceCurrency: typing.Optional[str] = None
    priceBreakdown: typing.Optional[typing.List[PriceBreakdownType]] = jstruct.JList[PriceBreakdownType]


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
    pickupCapabilities: typing.Optional[PickupCapabilitiesType] = jstruct.JStruct[PickupCapabilitiesType]
    deliveryCapabilities: typing.Optional[DeliveryCapabilitiesType] = jstruct.JStruct[DeliveryCapabilitiesType]


@attr.s(auto_attribs=True)
class RateResponseType:
    products: typing.Optional[typing.List[ProductType]] = jstruct.JList[ProductType]
