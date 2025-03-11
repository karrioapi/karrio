import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Dimensions:
    height: typing.Optional[float] = None
    length: typing.Optional[float] = None
    unit: typing.Optional[str] = None
    width: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Weight:
    unit: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ContainerSpecification:
    dimensions: typing.Optional[Dimensions] = jstruct.JStruct[Dimensions]
    weight: typing.Optional[Weight] = jstruct.JStruct[Weight]


@attr.s(auto_attribs=True)
class Ship:
    addressLine1: typing.Optional[str] = None
    city: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    name: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    stateOrRegion: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    email: typing.Optional[str] = None
    copyEmails: typing.Optional[typing.List[str]] = None
    phoneNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class RateRequest:
    containerSpecifications: typing.Optional[typing.List[ContainerSpecification]] = jstruct.JList[ContainerSpecification]
    serviceTypes: typing.Optional[typing.List[str]] = None
    shipFrom: typing.Optional[Ship] = jstruct.JStruct[Ship]
    shipTo: typing.Optional[Ship] = jstruct.JStruct[Ship]
    shipDate: typing.Optional[str] = None
