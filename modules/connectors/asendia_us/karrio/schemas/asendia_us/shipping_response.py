import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class LabelType:
    name: typing.Optional[str] = None
    type: typing.Optional[str] = None
    content: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PackageLabelType:
    packageId: typing.Optional[str] = None
    trackingNumber: typing.Optional[str] = None
    labels: typing.Optional[typing.List[LabelType]] = jstruct.JList[LabelType]


@attr.s(auto_attribs=True)
class ResponseStatusType:
    responseStatusCode: typing.Optional[str] = None
    responseStatusMessage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingRateType:
    productCode: typing.Optional[str] = None
    rate: typing.Optional[int] = None
    currencyType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ShippingResponseType:
    shippingRates: typing.Optional[typing.List[ShippingRateType]] = jstruct.JList[ShippingRateType]
    packageLabel: typing.Optional[PackageLabelType] = jstruct.JStruct[PackageLabelType]
    responseStatus: typing.Optional[ResponseStatusType] = jstruct.JStruct[ResponseStatusType]
