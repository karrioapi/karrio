import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class SizeOptions:
    length: typing.Optional[float] = None
    width: typing.Optional[float] = None
    height: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightOptions:
    weight: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Package:
    refNumber: typing.Optional[int] = None
    weightOptions: typing.Optional[WeightOptions] = jstruct.JStruct[WeightOptions]
    sizeOptions: typing.Optional[SizeOptions] = jstruct.JStruct[SizeOptions]


@attr.s(auto_attribs=True)
class RateRequest:
    postalCode: typing.Optional[str] = None
    originPostalCode: typing.Optional[str] = None
    packages: typing.Optional[typing.List[Package]] = jstruct.JList[Package]
