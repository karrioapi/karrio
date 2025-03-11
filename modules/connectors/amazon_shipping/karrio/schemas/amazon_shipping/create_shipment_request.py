import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class Dimensions:
    height: typing.Optional[float] = None
    length: typing.Optional[float] = None
    unit: typing.Optional[str] = None
    width: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Value:
    unit: typing.Optional[str] = None
    value: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Unit:
    value: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class UnitWeight:
    unit: typing.Optional[Unit] = jstruct.JStruct[Unit]
    value: typing.Optional[Unit] = jstruct.JStruct[Unit]


@attr.s(auto_attribs=True)
class Item:
    quantity: typing.Optional[float] = None
    title: typing.Optional[str] = None
    unitPrice: typing.Optional[Value] = jstruct.JStruct[Value]
    unitWeight: typing.Optional[UnitWeight] = jstruct.JStruct[UnitWeight]


@attr.s(auto_attribs=True)
class Container:
    containerReferenceId: typing.Optional[str] = None
    dimensions: typing.Optional[Dimensions] = jstruct.JStruct[Dimensions]
    items: typing.Optional[typing.List[Item]] = jstruct.JList[Item]
    value: typing.Optional[Value] = jstruct.JStruct[Value]
    weight: typing.Optional[Value] = jstruct.JStruct[Value]
    containerType: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class Ship:
    addressLine1: typing.Optional[str] = None
    city: typing.Optional[str] = None
    countryCode: typing.Optional[str] = None
    name: typing.Optional[str] = None
    postalCode: typing.Optional[str] = None
    stateOrRegion: typing.Optional[str] = None
    addressLine2: typing.Optional[str] = None
    addressLine3: typing.Optional[str] = None
    email: typing.Optional[str] = None
    copyEmails: typing.Optional[typing.List[str]] = None
    phoneNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CreateShipmentRequest:
    clientReferenceId: typing.Optional[str] = None
    containers: typing.Optional[typing.List[Container]] = jstruct.JList[Container]
    shipFrom: typing.Optional[Ship] = jstruct.JStruct[Ship]
    shipTo: typing.Optional[Ship] = jstruct.JStruct[Ship]
