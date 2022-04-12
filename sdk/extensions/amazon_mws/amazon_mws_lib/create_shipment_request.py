from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Dimensions:
    height: Optional[float] = None
    length: Optional[float] = None
    unit: Optional[str] = None
    width: Optional[float] = None


@s(auto_attribs=True)
class Value:
    unit: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class Unit:
    value: Optional[str] = None


@s(auto_attribs=True)
class UnitWeight:
    unit: Optional[Unit] = JStruct[Unit]
    value: Optional[Unit] = JStruct[Unit]


@s(auto_attribs=True)
class Item:
    quantity: Optional[float] = None
    title: Optional[str] = None
    unitPrice: Optional[Value] = JStruct[Value]
    unitWeight: Optional[UnitWeight] = JStruct[UnitWeight]


@s(auto_attribs=True)
class Container:
    containerReferenceId: Optional[str] = None
    dimensions: Optional[Dimensions] = JStruct[Dimensions]
    items: List[Item] = JList[Item]
    value: Optional[Value] = JStruct[Value]
    weight: Optional[Value] = JStruct[Value]
    containerType: Optional[str] = None


@s(auto_attribs=True)
class Ship:
    addressLine1: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = None
    name: Optional[str] = None
    postalCode: Optional[str] = None
    stateOrRegion: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    email: Optional[str] = None
    copyEmails: List[str] = []
    phoneNumber: Optional[str] = None


@s(auto_attribs=True)
class CreateShipmentRequest:
    clientReferenceId: Optional[str] = None
    containers: List[Container] = JList[Container]
    shipFrom: Optional[Ship] = JStruct[Ship]
    shipTo: Optional[Ship] = JStruct[Ship]
