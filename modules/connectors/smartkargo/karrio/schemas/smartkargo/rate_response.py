import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DetailType:
    slaInDays: typing.Optional[int] = None
    deliveryDateBasedOnShipment: typing.Optional[str] = None
    serviceType: typing.Optional[str] = None
    total: typing.Optional[float] = None
    totalTax: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    headerReference: typing.Optional[str] = None
    packageReference: typing.Optional[str] = None
    status: typing.Optional[str] = None
    details: typing.Optional[typing.List[DetailType]] = jstruct.JList[DetailType]
    validations: typing.Any = None
