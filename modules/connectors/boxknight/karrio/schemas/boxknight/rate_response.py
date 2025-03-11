import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Rate:
    price: typing.Optional[int] = None
    service: typing.Optional[str] = None
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    estimateDay: typing.Optional[str] = None
    estimateFrom: typing.Optional[str] = None
    estimateTo: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponse:
    rates: typing.Optional[typing.List[Rate]] = jstruct.JList[Rate]
