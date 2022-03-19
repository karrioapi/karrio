from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class Dimensions:
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    unit: Optional[str] = None


@s(auto_attribs=True)
class Value:
    value: Optional[int] = None
    unit: Optional[str] = None


@s(auto_attribs=True)
class Item:
    quantity: Optional[int] = None
    unitPrice: Optional[Value] = JStruct[Value]
    unitWeight: Optional[Value] = JStruct[Value]
    title: Optional[str] = None


@s(auto_attribs=True)
class Container:
    containerType: Optional[str] = None
    containerReferenceId: Optional[str] = None
    value: Optional[Value] = JStruct[Value]
    dimensions: Optional[Dimensions] = JStruct[Dimensions]
    items: List[Item] = JList[Item]
    weight: Optional[Value] = JStruct[Value]


@s(auto_attribs=True)
class Ship:
    name: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    addressLine3: Optional[str] = None
    stateOrRegion: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = None
    postalCode: Optional[str] = None
    email: Optional[str] = None
    copyEmails: List[str] = JList[str]
    phoneNumber: Optional[str] = None


@s(auto_attribs=True)
class CreateShipmentRequest:
    clientReferenceId: Optional[str] = None
    shipTo: Optional[Ship] = JStruct[Ship]
    shipFrom: Optional[Ship] = JStruct[Ship]
    containers: List[Container] = JList[Container]
