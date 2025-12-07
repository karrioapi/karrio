import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AddressValidationRequestType:
    type: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    cityName: typing.Optional[str] = None
