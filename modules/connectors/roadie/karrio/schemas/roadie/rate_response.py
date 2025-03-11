import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class RateResponse:
    price: typing.Optional[float] = None
    size: typing.Optional[str] = None
    estimated_distance: typing.Optional[float] = None
