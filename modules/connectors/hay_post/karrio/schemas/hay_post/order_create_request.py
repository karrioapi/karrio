import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ReceiverInfoType:
    companyName: typing.Optional[str] = None
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class NAddressType:
    countryId: typing.Optional[int] = None
    provinceStateId: typing.Optional[int] = None
    cityVillage: typing.Optional[str] = None
    street: typing.Optional[str] = None
    building: typing.Optional[int] = None
    apartment: typing.Optional[int] = None
    postalCode: typing.Optional[str] = None
    receiverInfo: typing.Optional[ReceiverInfoType] = jstruct.JStruct[ReceiverInfoType]


@attr.s(auto_attribs=True)
class OrderCreateRequestType:
    customerId: typing.Optional[int] = None
    serviceCategoryDirectionId: typing.Optional[int] = None
    weight: typing.Optional[int] = None
    comment: typing.Optional[str] = None
    returnRegisteredAddress: typing.Optional[bool] = None
    destinationAddress: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    returnAddress: typing.Optional[NAddressType] = jstruct.JStruct[NAddressType]
    additionalServices: typing.Optional[typing.List[int]] = None
