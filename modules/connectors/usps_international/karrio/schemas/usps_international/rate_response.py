import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class WarningType:
    warningCode: typing.Optional[str] = None
    warningDescription: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ExtraServiceType:
    extraService: typing.Optional[int] = None
    name: typing.Optional[str] = None
    priceType: typing.Optional[str] = None
    price: typing.Optional[float] = None
    warnings: typing.Optional[typing.List[WarningType]] = jstruct.JList[WarningType]
    SKU: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FeeType:
    name: typing.Optional[str] = None
    SKU: typing.Optional[str] = None
    price: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class RateType:
    description: typing.Optional[str] = None
    priceType: typing.Optional[str] = None
    price: typing.Optional[float] = None
    weight: typing.Optional[float] = None
    dimWeight: typing.Optional[float] = None
    fees: typing.Optional[typing.List[FeeType]] = jstruct.JList[FeeType]
    startDate: typing.Optional[str] = None
    endDate: typing.Optional[str] = None
    mailClass: typing.Optional[str] = None
    zone: typing.Optional[str] = None
    productName: typing.Optional[str] = None
    productDefinition: typing.Optional[str] = None
    processingCategory: typing.Optional[str] = None
    rateIndicator: typing.Optional[str] = None
    destinationEntryFacilityType: typing.Optional[str] = None
    SKU: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateOptionType:
    totalBasePrice: typing.Optional[float] = None
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]
    extraServices: typing.Optional[typing.List[ExtraServiceType]] = jstruct.JList[ExtraServiceType]


@attr.s(auto_attribs=True)
class RateResponseType:
    rateOptions: typing.Optional[typing.List[RateOptionType]] = jstruct.JList[RateOptionType]
