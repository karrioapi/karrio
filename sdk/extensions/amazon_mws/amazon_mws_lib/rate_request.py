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
class Weight:
    unit: Optional[str] = None
    value: Optional[float] = None


@s(auto_attribs=True)
class ContainerSpecification:
    dimensions: Optional[Dimensions] = JStruct[Dimensions]
    weight: Optional[Weight] = JStruct[Weight]


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
class RateRequest:
    containerSpecifications: List[ContainerSpecification] = JList[ContainerSpecification]
    serviceTypes: List[str] = []
    shipFrom: Optional[Ship] = JStruct[Ship]
    shipTo: Optional[Ship] = JStruct[Ship]
    shipDate: Optional[str] = None
