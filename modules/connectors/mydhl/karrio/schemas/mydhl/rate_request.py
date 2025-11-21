import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AccountType:
    typeCode: typing.Optional[str] = None
    number: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErDetailsType:
    postalCode: typing.Optional[str] = None
    cityName: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CustomerDetailsType:
    shipperDetails: typing.Optional[ErDetailsType] = jstruct.JStruct[ErDetailsType]
    receiverDetails: typing.Optional[ErDetailsType] = jstruct.JStruct[ErDetailsType]


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PackageType:
    typeCode: typing.Optional[str] = None
    weight: typing.Optional[float] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class RateRequestType:
    customerDetails: typing.Optional[CustomerDetailsType] = jstruct.JStruct[CustomerDetailsType]
    accounts: typing.Optional[typing.List[AccountType]] = jstruct.JList[AccountType]
    productCode: typing.Optional[str] = None
    localProductCode: typing.Optional[str] = None
    plannedShippingDateAndTime: typing.Optional[str] = None
    unitOfMeasurement: typing.Optional[str] = None
    isCustomsDeclarable: typing.Optional[bool] = None
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
