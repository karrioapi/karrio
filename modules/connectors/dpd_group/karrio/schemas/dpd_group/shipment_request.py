import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ParcelType:
    weight: typing.Optional[float] = None
    length: typing.Optional[int] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None
    content: typing.Optional[str] = None
    customerReferenceNumber1: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ErAddressType:
    name: typing.Optional[str] = None
    company: typing.Optional[str] = None
    street: typing.Optional[str] = None
    houseNumber: typing.Optional[int] = None
    postalCode: typing.Optional[int] = None
    city: typing.Optional[str] = None
    country: typing.Optional[str] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class InsuranceType:
    value: typing.Optional[float] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ServicesType:
    saturdayDelivery: typing.Optional[bool] = None
    insurance: typing.Optional[InsuranceType] = jstruct.JStruct[InsuranceType]


@attr.s(auto_attribs=True)
class ShipmentRequestType:
    shipperAddress: typing.Optional[ErAddressType] = jstruct.JStruct[ErAddressType]
    receiverAddress: typing.Optional[ErAddressType] = jstruct.JStruct[ErAddressType]
    parcels: typing.Optional[typing.List[ParcelType]] = jstruct.JList[ParcelType]
    productCode: typing.Optional[str] = None
    orderNumber: typing.Optional[str] = None
    shipmentDate: typing.Optional[str] = None
    labelFormat: typing.Optional[str] = None
    services: typing.Optional[ServicesType] = jstruct.JStruct[ServicesType]
