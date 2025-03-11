import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ResponseStatusType:
    responseStatusCode: typing.Optional[str] = None
    responseStatusMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRateType:
    productCode: typing.Optional[str] = None
    rate: typing.Optional[float] = None
    currencyType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    shippingRates: typing.Optional[typing.List[ShippingRateType]] = jstruct.JList[ShippingRateType]
    responseStatus: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
