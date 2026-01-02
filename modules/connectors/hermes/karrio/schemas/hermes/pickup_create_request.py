import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ParcelCountType:
    pickupParcelCountXS: typing.Optional[int] = None
    pickupParcelCountS: typing.Optional[int] = None
    pickupParcelCountM: typing.Optional[int] = None
    pickupParcelCountL: typing.Optional[int] = None
    pickupParcelCountXL: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupAddressType:
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    town: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    addressAddition: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupNameType:
    title: typing.Optional[str] = None
    gender: typing.Optional[str] = None
    firstname: typing.Optional[str] = None
    middlename: typing.Optional[str] = None
    lastname: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupCreateRequestType:
    pickupAddress: typing.Optional[PickupAddressType] = jstruct.JStruct[PickupAddressType]
    pickupName: typing.Optional[PickupNameType] = jstruct.JStruct[PickupNameType]
    phone: typing.Optional[str] = None
    pickupDate: typing.Optional[str] = None
    pickupTimeSlot: typing.Optional[str] = None
    parcelCount: typing.Optional[ParcelCountType] = jstruct.JStruct[ParcelCountType]
