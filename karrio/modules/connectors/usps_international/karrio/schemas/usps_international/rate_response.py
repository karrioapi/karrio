import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PaymentAccountType:
    accountType: typing.Optional[str] = None
    accountNumber: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class WarningType:
    warningCode: typing.Optional[str] = None
    warningDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExtraServiceType:
    name: typing.Optional[str] = None
    price: typing.Optional[float] = None
    extraService: typing.Optional[int] = None
    priceType: typing.Optional[str] = None
    warnings: typing.Optional[typing.List[WarningType]] = jstruct.JList[WarningType]
    SKU: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateType:
    description: typing.Optional[str] = None
    startDate: typing.Optional[str] = None
    endDate: typing.Optional[str] = None
    price: typing.Optional[float] = None
    zone: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensionalWeight: typing.Optional[int] = None
    dimWeight: typing.Optional[int] = None
    fees: typing.Optional[typing.List[typing.Any]] = None
    priceType: typing.Optional[str] = None
    mailClass: typing.Optional[str] = None
    productName: typing.Optional[str] = None
    productDefinition: typing.Optional[str] = None
    processingCategory: typing.Optional[str] = None
    rateIndicator: typing.Optional[str] = None
    destinationEntryFacilityType: typing.Optional[str] = None
    SKU: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateOptionType:
    totalPrice: typing.Optional[float] = None
    totalBasePrice: typing.Optional[float] = None
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]
    extraServices: typing.Optional[typing.List[ExtraServiceType]] = jstruct.JList[ExtraServiceType]


@attr.s(auto_attribs=True)
class ShippingOptionType:
    mailClass: typing.Optional[str] = None
    rateOptions: typing.Optional[typing.List[RateOptionType]] = jstruct.JList[RateOptionType]


@attr.s(auto_attribs=True)
class PricingOptionType:
    shippingOptions: typing.Optional[typing.List[ShippingOptionType]] = jstruct.JList[ShippingOptionType]
    priceType: typing.Optional[str] = None
    paymentAccount: typing.Optional[PaymentAccountType] = jstruct.JStruct[PaymentAccountType]


@attr.s(auto_attribs=True)
class RateResponseType:
    originZIPCode: typing.Optional[int] = None
    foreignPostalCode: typing.Optional[int] = None
    destinationCountryCode: typing.Optional[str] = None
    pricingOptions: typing.Optional[typing.List[PricingOptionType]] = jstruct.JList[PricingOptionType]
