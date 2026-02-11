import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CustomerInfosType:
    customerAccountNumber: typing.Optional[str] = None
    customerSubAccountNumber: typing.Optional[str] = None
    customerID: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class MessageType:
    messageType: typing.Optional[str] = None
    messageDestination: typing.Optional[str] = None
    messageLanguage: typing.Optional[str] = None
    senderCompany: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelMaxDimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class PickupType:
    date: typing.Optional[str] = None
    fromTime: typing.Optional[str] = None
    toTime: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupAddressType:
    companyName: typing.Optional[str] = None
    name1: typing.Optional[str] = None
    name2: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    addressLine1: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    interphoneName: typing.Optional[str] = None
    floor: typing.Optional[str] = None
    doorCode: typing.Optional[str] = None
    building: typing.Optional[str] = None
    department: typing.Optional[str] = None
    country: typing.Optional[str] = None
    state: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    city: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupContactType:
    contactPerson: typing.Optional[str] = None
    phone1: typing.Optional[str] = None
    phone2: typing.Optional[str] = None
    fax: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PickupCreateRequestType:
    customerInfos: typing.Optional[CustomerInfosType] = jstruct.JStruct[CustomerInfosType]
    shipmentNumbers: typing.Optional[typing.List[str]] = None
    parcelNumbers: typing.Optional[typing.List[str]] = None
    pickup: typing.Optional[PickupType] = jstruct.JStruct[PickupType]
    numberOfParcels: typing.Optional[int] = None
    addressId: typing.Optional[str] = None
    pickupAddress: typing.Optional[PickupAddressType] = jstruct.JStruct[PickupAddressType]
    pickupContact: typing.Optional[PickupContactType] = jstruct.JStruct[PickupContactType]
    pickupWeight: typing.Optional[str] = None
    parcelMaxWeight: typing.Optional[str] = None
    parcelMaxDimensions: typing.Optional[ParcelMaxDimensionsType] = jstruct.JStruct[ParcelMaxDimensionsType]
    comment: typing.Optional[str] = None
    references: typing.Optional[typing.List[str]] = None
    sendingDepot: typing.Optional[str] = None
    messages: typing.Optional[typing.List[MessageType]] = jstruct.JList[MessageType]
