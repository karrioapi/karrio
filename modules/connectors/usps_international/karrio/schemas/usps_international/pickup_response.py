import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PackageType:
    packageType: typing.Optional[str] = None
    packageCount: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class AddressType:
    streetAddress: typing.Optional[str] = None
    streetAddressAbbreviation: typing.Optional[str] = None
    secondaryAddress: typing.Optional[str] = None
    cityAbbreviation: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    ZIPCode: typing.Optional[str] = None
    ZIPPlus4: typing.Optional[str] = None
    urbanization: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactType:
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupAddressType:
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    firm: typing.Optional[str] = None
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[typing.List[ContactType]] = jstruct.JList[ContactType]


@attr.s(auto_attribs=True)
class PickupLocationType:
    packageLocation: typing.Optional[str] = None
    specialInstructions: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CarrierPickupRequestType:
    pickupDate: typing.Optional[str] = None
    pickupAddress: typing.Optional[PickupAddressType] = jstruct.JStruct[PickupAddressType]
    packages: typing.Optional[typing.List[PackageType]] = jstruct.JList[PackageType]
    estimatedWeight: typing.Optional[int] = None
    pickupLocation: typing.Optional[PickupLocationType] = jstruct.JStruct[PickupLocationType]


@attr.s(auto_attribs=True)
class PickupResponseType:
    confirmationNumber: typing.Optional[str] = None
    pickupDate: typing.Optional[str] = None
    carrierPickupRequest: typing.Optional[CarrierPickupRequestType] = jstruct.JStruct[CarrierPickupRequestType]
