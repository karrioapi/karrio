import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class WeightType:
    value: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ChargeType:
    name: typing.Optional[str] = None
    amount: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    rate: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class CommodityType:
    itemNumber: typing.Optional[int] = None
    title: typing.Optional[str] = None
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]
    restrictions: typing.Optional[typing.List[typing.Any]] = None


@attr.s(auto_attribs=True)
class MessageType:
    code: typing.Optional[int] = None
    level: typing.Optional[str] = None
    timestamp: typing.Optional[str] = None
    message: typing.Optional[str] = None
    details: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ServiceType:
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None
    checkoutName: typing.Optional[str] = None
    description: typing.Optional[str] = None
    transit: typing.Optional[int] = None
    dispatchDays: typing.Optional[int] = None
    includeFirstMile: typing.Optional[bool] = None
    isActive: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class RateType:
    price: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    transit: typing.Optional[int] = None
    estimatedDelivery: typing.Optional[str] = None
    service: typing.Optional[ServiceType] = jstruct.JStruct[ServiceType]
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]


@attr.s(auto_attribs=True)
class RateResponseType:
    messages: typing.Optional[typing.List[MessageType]] = jstruct.JList[MessageType]
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    scaleWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    dimWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    billWeight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
