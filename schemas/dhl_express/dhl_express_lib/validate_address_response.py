from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ServiceArea:
    code: Optional[str] = None
    description: Optional[str] = None
    GMTOffset: Optional[str] = None


@s(auto_attribs=True)
class Address:
    countryCode: Optional[str] = None
    postalCode: Optional[int] = None
    cityName: Optional[str] = None
    countyName: Optional[str] = None
    serviceArea: Optional[ServiceArea] = JStruct[ServiceArea]


@s(auto_attribs=True)
class ValidateAddressResponse:
    warnings: List[str] = JList[str]
    address: List[Address] = JList[Address]
