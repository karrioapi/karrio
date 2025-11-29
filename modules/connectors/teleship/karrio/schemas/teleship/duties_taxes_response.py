import attr
import jstruct
import typing


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
class DutiesTaxesResponseType:
    messages: typing.Optional[typing.List[typing.Any]] = None
    price: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    charges: typing.Optional[typing.List[ChargeType]] = jstruct.JList[ChargeType]
    commodities: typing.Optional[typing.List[CommodityType]] = jstruct.JList[CommodityType]
