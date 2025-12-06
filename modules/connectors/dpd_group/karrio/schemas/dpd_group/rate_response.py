import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class RateType:
    productCode: typing.Optional[str] = None
    productName: typing.Optional[str] = None
    totalAmount: typing.Optional[float] = None
    currency: typing.Optional[str] = None
    transitDays: typing.Optional[int] = None
    deliveryDate: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]
