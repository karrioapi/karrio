import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ChargeType:
    name: typing.Optional[str] = None
    amount: typing.Optional[float] = None
    rate: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CommodityType:
    itemNumber: typing.Optional[int] = None
    title: typing.Optional[str] = None
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]


@attr.s(auto_attribs=True)
class MessageType:
    code: typing.Optional[int] = None
    timestamp: typing.Optional[str] = None
    message: typing.Optional[str] = None
    details: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class ServiceType:
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateType:
    price: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    transit: typing.Optional[int] = None
    service: typing.Optional[ServiceType] = jstruct.JStruct[ServiceType]
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]
    estimatedDelivery: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
    messages: typing.Optional[typing.List[MessageType]] = jstruct.JList[MessageType]
