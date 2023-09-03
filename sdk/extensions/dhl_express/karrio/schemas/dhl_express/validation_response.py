from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ServiceAreaType:
    code: Optional[str] = None
    description: Optional[str] = None
    GMTOffset: Optional[str] = None


@s(auto_attribs=True)
class AddressType:
    countryCode: Optional[str] = None
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    countyName: Optional[str] = None
    serviceArea: Optional[ServiceAreaType] = JStruct[ServiceAreaType]


@s(auto_attribs=True)
class ValidationResponseType:
    warnings: List[str] = []
    address: List[AddressType] = JList[AddressType]
