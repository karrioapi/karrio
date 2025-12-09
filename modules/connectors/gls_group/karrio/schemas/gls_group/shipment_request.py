import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ReferenceType:
    type: typing.Optional[str] = None
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    weight: typing.Optional[float] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    references: typing.Optional[typing.List[ReferenceType]] = jstruct.JList[ReferenceType]


@attr.s(auto_attribs=True)
class PrintingOptionsType:
    templateName: typing.Optional[str] = None
    printerLanguage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ReceiverType:
    name1: typing.Optional[str] = None
    name2: typing.Optional[str] = None
    name3: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[str] = None
    zipCode: typing.Optional[str] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None
    contactPerson: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DetailsType:
    pass


@attr.s(auto_attribs=True)
class ServiceType:
    type: typing.Optional[str] = None
    details: typing.Optional[DetailsType] = jstruct.JStruct[DetailsType]


@attr.s(auto_attribs=True)
class ShipmentType:
    product: typing.Optional[str] = None
    sender: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    receiver: typing.Optional[ReceiverType] = jstruct.JStruct[ReceiverType]
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    services: typing.Optional[typing.List[ServiceType]] = jstruct.JList[ServiceType]
    shippingDate: typing.Optional[str] = None
    references: typing.Optional[typing.List[ReferenceType]] = jstruct.JList[ReferenceType]
    labelFormat: typing.Optional[str] = None
    printingOptions: typing.Optional[PrintingOptionsType] = jstruct.JStruct[PrintingOptionsType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    shipment: typing.Optional[ShipmentType] = jstruct.JStruct[ShipmentType]
