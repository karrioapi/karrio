import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class SurchargeType:
    name: typing.Optional[str] = None
    amount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class QuoteType:
    carrierName: typing.Optional[str] = None
    serviceId: typing.Optional[int] = None
    serviceName: typing.Optional[str] = None
    deliveryCarrier: typing.Optional[str] = None
    modeTransport: typing.Optional[str] = None
    transitDays: typing.Optional[str] = None
    baseCharge: typing.Optional[int] = None
    fuelSurcharge: typing.Optional[int] = None
    fuelSurchargePercentage: typing.Optional[int] = None
    carbonNeutralFees: typing.Optional[int] = None
    surcharges: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    totalCharge: typing.Optional[int] = None
    processingFees: typing.Optional[int] = None
    taxes: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    totalChargedAmount: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    uuid: typing.Optional[str] = None
    quotes: typing.Optional[typing.List[QuoteType]] = jstruct.JList[QuoteType]
    warnings: typing.Optional[typing.List[str]] = None
    errors: typing.Optional[typing.List[str]] = None
