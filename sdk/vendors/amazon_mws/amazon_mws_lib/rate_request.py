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
class Weight:
    unit: Optional[str] = None
    value: Optional[int] = None


@s(auto_attribs=True)
class ContainerSpecification:
    dimensions: Optional[Dimensions] = JStruct[Dimensions]
    weight: Optional[Weight] = JStruct[Weight]


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
class RateRequest:
    shipTo: Optional[Ship] = JStruct[Ship]
    shipFrom: Optional[Ship] = JStruct[Ship]
    serviceTypes: List[str] = JList[str]
    shipDate: Optional[str] = None
    containerSpecifications: List[ContainerSpecification] = JList[ContainerSpecification]
