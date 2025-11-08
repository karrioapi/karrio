import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ServiceAreaType:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    facilityCode: typing.Optional[str] = None
    inboundSortCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    postalCode: typing.Optional[int] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    countyName: typing.Optional[str] = None
    serviceArea: typing.Optional[ServiceAreaType] = jstruct.JStruct[ServiceAreaType]


@attr.s(auto_attribs=True)
class AddressValidationResponseType:
    warnings: typing.Optional[typing.List[typing.Any]] = None
    address: typing.Optional[typing.List[AddressType]] = jstruct.JList[AddressType]
