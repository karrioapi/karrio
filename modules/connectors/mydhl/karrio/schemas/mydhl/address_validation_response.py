import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ServiceAreaType:
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    GMTOffset: typing.Optional[str] = None
    facilityCode: typing.Optional[str] = None
    inboundSortCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    countryCode: typing.Optional[str] = None
    postalCode: typing.Optional[int] = None
    cityName: typing.Optional[str] = None
    countyName: typing.Optional[str] = None
    serviceArea: typing.Optional[ServiceAreaType] = jstruct.JStruct[ServiceAreaType]


@attr.s(auto_attribs=True)
class AddressValidationResponseType:
    warnings: typing.Optional[typing.List[str]] = None
    address: typing.Optional[typing.List[AddressType]] = jstruct.JList[AddressType]
