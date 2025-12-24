import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DimensionsType:
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class ParcelInfosType:
    weight: typing.Optional[str] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ParcelType:
    parcelInfos: typing.Optional[ParcelInfosType] = jstruct.JStruct[ParcelInfosType]
    parcelContent: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AddressType:
    companyName: typing.Optional[str] = None
    name1: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContactType:
    phone1: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverType:
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]


@attr.s(auto_attribs=True)
class CustomerInfosType:
    customerID: typing.Optional[str] = None
    customerAccountNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SenderType:
    customerInfos: typing.Optional[CustomerInfosType] = jstruct.JStruct[CustomerInfosType]
    address: typing.Optional[AddressType] = jstruct.JStruct[AddressType]
    contact: typing.Optional[ContactType] = jstruct.JStruct[ContactType]


@attr.s(auto_attribs=True)
class ShipmentInfosType:
    productCode: typing.Optional[str] = None
    shipmentId: typing.Optional[str] = None
    weight: typing.Optional[str] = None
    dimensions: typing.Optional[DimensionsType] = jstruct.JStruct[DimensionsType]


@attr.s(auto_attribs=True)
class ShipmentRequestElementType:
    numberOfParcels: typing.Optional[str] = None
    shipmentInfos: typing.Optional[ShipmentInfosType] = jstruct.JStruct[ShipmentInfosType]
    sender: typing.Optional[SenderType] = jstruct.JStruct[SenderType]
    receiver: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    parcel: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
